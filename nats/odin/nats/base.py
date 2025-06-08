"""
Skeleton implementation of a speech‑to‑speech pipeline orchestration layer on top of
NATS + JetStream.  The goal is to show the _shape_ of the classes and the request‑reply
flow that we have been discussing – you will almost certainly adapt details (logging,
error handling, protobufs, metrics, tracing) to your own stack.

External deps assumed:
* nats‑py (async client)             pip install nats-py
* your generated protobufs           from odin-proto package

The code purposefully avoids concrete audio / ML logic; you plug that into concrete
subclasses of `BaseSession`.
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from enum import IntEnum
from typing import Dict, Any, List, Optional

from nats.aio.client import Client as NATS
# Import from the odin-proto package
from odin.v1 import session_pb2 as pb

log = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# 1) Shared status enum (short‑hand – you already have it in the proto)
# ---------------------------------------------------------------------------
class ModuleStatus(IntEnum):
    INITIALIZING = 0
    RUNNING = 1
    FAILED = 2
    DISCONNECTED = 3


# ---------------------------------------------------------------------------
# 2) BaseSession – one logical session of **this module**
# ---------------------------------------------------------------------------
class BaseSession(ABC):
    """Lifecycle wrapper around whatever engine you run per session (STT, TTS …)."""

    def __init__(self, session_id: str, config: bytes, nc: NATS, module_name: str):
        self.session_id = session_id
        self.config = config            # opaque – pass to your engine as you wish
        self.nc = nc
        self.module_name = module_name

    # ---- abstract hooks --------------------------------------------------
    @abstractmethod
    async def initialize(self) -> None:
        """Start / warm‑up the underlying engine, allocate resources."""

    @abstractmethod
    async def cleanup(self) -> None:
        """Free resources, flush buffers, close files."""

    # ---- helper to send **durable** status updates -----------------------
    async def publish_status(self, status: ModuleStatus, detail: str = "") -> None:
        """Emit a Status message to `session.<id>.<module>.status` (regular NATS)."""
        log.debug(f"Publishing status {status} for {self.module_name} in session {self.session_id}")
        subj = f"session.{self.session_id}.{self.module_name}.status"
        msg = pb.Status(
            session_id=self.session_id,
            module=self.module_name,
            status=status,
            detail=detail,
        ).SerializeToString()
        await self.nc.publish(subj, msg)
        log.debug(f"Published status {status} to subject {subj}")


# ---------------------------------------------------------------------------
# 3) BaseModule – queue‑group worker that spawns BaseSessions
# ---------------------------------------------------------------------------
class BaseModule(ABC):
    """Generic worker that subscribes to `session.*.<module>.cmd` and handles
    Init / Shutdown commands via Core‑NATS request‑reply.
    """

    def __init__(self, nc: NATS, name: str, queue_group: Optional[str] = None):
        self.nc = nc
        self.name = name
        self.queue_group = queue_group or f"{name}_workers"
        self.sessions: Dict[str, BaseSession] = {}

    # ---- public bootstrap -----------------------------------------------
    async def start(self) -> None:
        subj = f"session.*.{self.name}.cmd"
        # Queue group so multiple replicas share the load.
        await self.nc.subscribe(subj, queue=self.queue_group, cb=self._on_command)  # type: ignore[arg-type]
        log.info("%s subscribed on %s (q=%s)", self.name, subj, self.queue_group)

    # ---- NATS message callback ------------------------------------------
    async def _on_command(self, msg):  # noqa: ANN001 – nats.Msg
        """Handle Init / Shutdown commands coming from the SessionManager."""
        log.debug(f"{self.name} received command on subject: {msg.subject}")
        
        try:
            cmd = pb.Command.FromString(msg.data)
            log.debug(f"{self.name} parsed command successfully")
        except Exception as e:
            log.error(f"{self.name} failed to parse command: {e}")
            return

        if cmd.HasField("init"):
            sess_id = cmd.init.session_id
            cfg = cmd.init.config
            log.debug(f"{self.name} handling init command for session {sess_id}")
            await self._handle_init(sess_id, cfg, msg.reply)
        elif cmd.HasField("shutdown"):
            sess_id = cmd.shutdown.session_id
            log.debug(f"{self.name} handling shutdown command for session {sess_id}")
            await self._handle_shutdown(sess_id, msg.reply)
        else:
            log.warning("Unknown command received by %s", self.name)

    # ---- command handlers ----------------------------------------------
    async def _handle_init(self, sess_id: str, cfg: bytes, reply: str) -> None:
        try:
            log.debug(f"Handling init for session {sess_id}, reply subject: {reply}")
            
            # Quick ACK so requester can unblock - use regular NATS, not JetStream
            await self.nc.publish(reply, pb.Status(
                session_id=sess_id,
                module=self.name,
                status=ModuleStatus.INITIALIZING,
            ).SerializeToString())
            log.debug(f"Sent INITIALIZING status for {self.name}")

            session = await self.create_session(sess_id, cfg)
            log.debug(f"Created session object for {self.name}")
            self.sessions[sess_id] = session

            log.debug(f"Starting initialization for {self.name}")
            await session.initialize()
            log.debug(f"Completed initialization for {self.name}")
            
            # This one uses regular NATS for status updates
            await asyncio.sleep(1)
            await session.publish_status(ModuleStatus.RUNNING)
            log.info("%s – session %s RUNNING", self.name, sess_id)

        except Exception as exc:  # noqa: BLE001
            err = str(exc)
            log.error(f"Exception during init for {self.name}: {err}", exc_info=True)
            # Error reply via regular NATS (only if we haven't already replied)
            try:
                await self.nc.publish(reply, pb.Status(
                    session_id=sess_id,
                    module=self.name,
                    status=ModuleStatus.FAILED,
                    detail=err,
                ).SerializeToString())
            except:
                pass  # Already replied
            log.exception("%s – session %s FAILED: %s", self.name, sess_id, err)

    async def _handle_shutdown(self, sess_id: str, reply: str) -> None:
        session = self.sessions.pop(sess_id, None)
        if session is None:
            # Nothing to clean, but still respond so SessionManager unblocks.
            await self.nc.publish(reply, pb.Status(
                session_id=sess_id,
                module=self.name,
                status=ModuleStatus.DISCONNECTED,
                detail="unknown session",
            ).SerializeToString())
            return

        await session.cleanup()
        await session.publish_status(ModuleStatus.DISCONNECTED)
        await self.nc.publish(reply, pb.Status(
            session_id=sess_id,
            module=self.name,
            status=ModuleStatus.DISCONNECTED,
        ).SerializeToString())
        log.info("%s – session %s disconnected", self.name, sess_id)

    # ---- factory for concrete Session objects ---------------------------
    @abstractmethod
    async def create_session(self, sess_id: str, cfg: bytes) -> BaseSession:
        """Instantiate & return a subclass of BaseSession."""


# ---------------------------------------------------------------------------
# 4) SessionManager – orchestration layer used by your application backend
# ---------------------------------------------------------------------------
class SessionManager:
    """Start / stop multi‑module sessions and wait for them to become RUNNING."""

    def __init__(self, nc: NATS, modules: List[str]):
        self.nc = nc
        self.modules = modules

    # ---- public API ------------------------------------------------------
    async def start_session(self, sess_id: str, configs: Dict[str, bytes], *, timeout: float = 3.0) -> None:
        """Spin‑up *all* modules; raise if any fails."""

        # 1) Send Init commands in parallel and wait for INITIALIZING / FAILED replies.
        init_tasks: Dict[str, "asyncio.Task[bytes]"] = {}
        for m in self.modules:
            subj = f"session.{sess_id}.{m}.cmd"
            cmd = pb.Command(init=pb.Init(session_id=sess_id, config=configs[m]))
            log.debug(f"Sending init command to {subj}")
            init_tasks[m] = asyncio.create_task(
                self.nc.request(subj, cmd.SerializeToString(), timeout=timeout))

        # Gather first replies – they unblock the request‑reply wait.
        for m, t in init_tasks.items():
            try:
                log.debug(f"Waiting for reply from {m}")
                msg = await t
            except asyncio.TimeoutError as te:  # noqa: PERF203 – keep explicit
                raise RuntimeError(f"{m} did not ACK in {timeout}s") from te

            log.debug(f"Received reply from {m}, type: {type(msg)}")
            
            # Check if msg is bytes or a Message object
            if hasattr(msg, 'data'):
                data = msg.data
            else:
                data = msg
                
            log.debug(f"Reply data from {m}: {len(data)} bytes")
            try:
                st = pb.Status()
                st.ParseFromString(data)
                if st.status == ModuleStatus.FAILED:
                    raise RuntimeError(f"{m} failed during init: {st.detail}")
            except Exception as e:
                log.error(f"Failed to parse reply from {m}: {e}")
                log.error(f"Reply data (first 100 bytes): {data[:100]}")
                raise

        # 2) Wait until every module reports RUNNING via the durable status stream.
        await self._wait_for_running(sess_id)
        log.info("✅ Session %s READY", sess_id)

    async def stop_session(self, sess_id: str, *, timeout: float = 0.1) -> None:
        """Gracefully tear‑down all modules."""
        shutdown_tasks: Dict[str, "asyncio.Task[bytes]"] = {}
        for m in self.modules:
            subj = f"session.{sess_id}.{m}.cmd"
            cmd = pb.Command(shutdown=pb.Shutdown(session_id=sess_id))
            shutdown_tasks[m] = asyncio.create_task(
                self.nc.request(subj, cmd.SerializeToString(), timeout=timeout))

        for m, t in shutdown_tasks.items():
            try:
                msg = await t
            except asyncio.TimeoutError as te:  # noqa: PERF203
                raise RuntimeError(f"{m} did not ACK shutdown in {timeout}s") from te

            st = pb.Status()
            st.ParseFromString(msg.data)
            if st.status != ModuleStatus.DISCONNECTED:
                raise RuntimeError(f"{m} returned unexpected state {st.status}")

        log.info("🛑 Session %s fully disconnected", sess_id)

    # ---- internals -------------------------------------------------------
    async def _wait_for_running(self, sess_id: str) -> None:
        """Subscribe to `session.<id>.*.status` and resolve when all RUNNING."""
        subj = f"session.{sess_id}.*.status"
        sub = await self.nc.subscribe(subj)  # type: ignore[arg-type]
        states: Dict[str, ModuleStatus] = {m: ModuleStatus.INITIALIZING for m in self.modules}

        log.debug(f"Subscribed to {subj}... Waiting for RUNNING status")
        while True:
            try:
                # Wait for status messages with a longer timeout
                msg = await sub.next_msg(timeout=2.0)  # noqa: SLF001 – ok here
                
                # Debug logging
                log.debug(f"Received message on subject: {msg.subject}")
                log.debug(f"Message data length: {len(msg.data)} bytes")
                
                st = pb.Status()
                st.ParseFromString(msg.data)
                states[st.module] = st.status  # type: ignore[index]
                
                log.debug(f"Module {st.module} status: {st.status}")

                if all(s == ModuleStatus.RUNNING for s in states.values()):
                    await sub.unsubscribe()
                    return
            except asyncio.TimeoutError:
                # Check if we already have all modules in RUNNING state
                if all(s == ModuleStatus.RUNNING for s in states.values()):
                    await sub.unsubscribe()
                    return
                # Otherwise continue waiting
                continue
            except Exception as e:
                log.error(f"Failed to parse status message: {e}")
                await sub.unsubscribe()
                raise 
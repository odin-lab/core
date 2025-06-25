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
import time
import socket
from abc import ABC, abstractmethod
from enum import IntEnum
from typing import Dict, Any, List, Optional
import uuid

from nats.aio.client import Client as NATS
from nats.js import JetStreamContext
from nats.js.kv import KeyValue

# Import from the odin-proto package
from odin.nats.observability import setup_tracing
from odin.v1 import session_pb2 as session_dec


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

    def __init__(self, session_id: str, config: bytes, nc: NATS, instance_id: str):
        self.session_id = session_id
        self.config = config  # opaque – pass to your engine as you wish
        self.nc = nc
        self.instance_id = instance_id

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
        log.debug(
            f"Publishing status {status} for {self.instance_id} in session {self.session_id}"
        )
        subj = f"session.{self.session_id}.{self.instance_id}.status"
        msg = session_dec.Status(
            session_id=self.session_id,
            instance_id=self.instance_id,
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
    Now also publishes module bootup status to KV store.
    """

    nc: NATS
    type: session_dec.ModuleType
    name: str
    queue_group: str
    sessions: Dict[str, BaseSession]
    kv: Optional[KeyValue]
    heartbeat_task: Optional[asyncio.Task]
    version: str

    def __init__(
        self,
        nc: NATS,
        type: session_dec.ModuleType,
        name: str,
        queue_group: Optional[str] = None,
        version: str = "1.0.0",
        config_schema: str = "",
    ):
        self.nc = nc
        self.name = name
        self.type = type
        self.instance_id = f"{session_dec.ModuleType.Name(type).lower()}-{name}-{str(uuid.uuid4())[:6]}"
        self.queue_group = queue_group or f"{name}_workers"
        self.sessions: Dict[str, BaseSession] = {}
        self.version = version
        self.kv = None
        self.heartbeat_task = None
        self.config_schema = config_schema

        setup_tracing(self.instance_id)

    # ---- public bootstrap -----------------------------------------------
    async def start(self) -> None:
        # Initialize JetStream and KV store
        js = self.nc.jetstream()

        # Create or get the module registry KV bucket
        try:
            self.kv = await js.key_value("module_registry")
        except Exception:
            raise RuntimeError(
                "Failed to open module registry KV bucket! Is the server running and the bucket created?"
            )

        # Publish bootup message
        await self._publish_bootup()

        # Start heartbeat task
        self.heartbeat_task = asyncio.create_task(self._heartbeat_loop())

        # Subscribe to commands
        subj = f"session.*.{self.instance_id}.cmd"
        await self.nc.subscribe(subj, queue=self.queue_group, cb=self._on_command)
        log.info("%s subscribed on %s (q=%s)", self.instance_id, subj, self.queue_group)

    async def stop(self) -> None:
        """Graceful shutdown - remove from registry"""

        for sess_id, session in self.sessions.items():
            await self._handle_shutdown(sess_id, f"session.{sess_id}.{self.instance_id}.cmd")

        if self.heartbeat_task:
            self.heartbeat_task.cancel()
            try:
                await self.heartbeat_task
            except asyncio.CancelledError:
                pass

        # Remove from KV store
        if self.kv:
            await self.kv.purge(f"{self.instance_id}.bootup")
            await self.kv.purge(f"{self.instance_id}.heartbeat")
            log.info(f"Removed {self.instance_id} from registry")

    # ---- KV store operations --------------------------------------------
    async def _publish_bootup(self) -> None:
        """Publish module bootup information to KV store"""
        bootup = session_dec.ModuleBootup(
            type=self.type,
            name=self.name,
            instance_id=self.instance_id,
            started_at=int(time.time()),
            version=self.version,
            host=socket.gethostname(),
            config_schema=self.config_schema,
        )

        key = f"{self.instance_id}.bootup"
        await self.kv.put(key, bootup.SerializeToString())
        log.info(f"Published bootup for {self.instance_id}")

    async def _heartbeat_loop(self) -> None:
        """Periodically update heartbeat in KV store"""
        while True:
            try:

                heartbeat = session_dec.ModuleHeartbeat(
                    instance_id=self.instance_id,
                    timestamp=int(time.time()),
                    status=ModuleStatus.RUNNING,
                    active_sessions=len(self.sessions),
                )

                key = f"{self.instance_id}.heartbeat"
                await self.kv.put(key, heartbeat.SerializeToString())

                await asyncio.sleep(30)  # Heartbeat every 30 seconds

            except asyncio.CancelledError:
                break
            except Exception as e:
                log.error(f"Heartbeat error for {self.name}: {e}")

    # ---- NATS message callback ------------------------------------------
    async def _on_command(self, msg):  # noqa: ANN001 – nats.Msg
        """Handle Init / Shutdown commands coming from the SessionManager."""
        log.info(f"{self.name} received command on subject: {msg.subject}")

        try:
            cmd = session_dec.Command.FromString(msg.data)
            log.info(f"{self.name} parsed command successfully")
        except Exception as e:
            log.error(f"{self.name} failed to parse command: {e}")
            return

        if cmd.HasField("init"):
            sess_id = cmd.init.session_id
            cfg = cmd.init.config
            log.info(f"{self.name} handling init command for session {sess_id}")
            await self._handle_init(sess_id, cfg, msg.reply)
        elif cmd.HasField("shutdown"):
            sess_id = cmd.shutdown.session_id
            log.info(f"{self.name} handling shutdown command for session {sess_id}")
            await self._handle_shutdown(sess_id, msg.reply)
        else:
            log.warning("Unknown command received by %s", self.name)

    # ---- command handlers ----------------------------------------------
    async def _handle_init(self, sess_id: str, cfg: bytes, reply: str) -> None:
        try:
            log.info(f"Handling init for session {sess_id}, reply subject: {reply}")

            # Quick ACK so requester can unblock - use regular NATS, not JetStream
            await self.nc.publish(
                reply,
                session_dec.Status(
                    session_id=sess_id,
                    instance_id=self.instance_id,
                    status=ModuleStatus.INITIALIZING,
                ).SerializeToString(),
            )
            log.info(f"Sent INITIALIZING status for {self.name}")

            session = await self.create_session(sess_id, cfg)
            log.info(f"Created session object for {self.name}")
            self.sessions[sess_id] = session

            log.info(f"Starting initialization for {self.name}")
            await session.initialize()
            log.info(f"Completed initialization for {self.name}")

            # This one uses regular NATS for status updates
            await session.publish_status(ModuleStatus.RUNNING)
            log.info("%s – session %s RUNNING", self.name, sess_id)

        except Exception as exc:  # noqa: BLE001
            err = str(exc)
            log.error(f"Exception during init for {self.name}: {err}", exc_info=True)
            # Error reply via regular NATS (only if we haven't already replied)
            try:
                await self.nc.publish(
                    reply,
                    session_dec.Status(
                        session_id=sess_id,
                        instance_id=self.instance_id,
                        status=ModuleStatus.FAILED,
                        detail=err,
                    ).SerializeToString(),
                )
            except:
                pass  # Already replied
            log.exception("%s – session %s FAILED: %s", self.name, sess_id, err)

    async def _handle_shutdown(self, sess_id: str, reply: str) -> None:
        session = self.sessions.pop(sess_id, None)
        if session is None:
            # Nothing to clean, but still respond so SessionManager unblocks.
            await self.nc.publish(
                reply,
                session_dec.Status(
                    session_id=sess_id,
                    instance_id=self.instance_id,
                    status=ModuleStatus.DISCONNECTED,
                    detail="unknown session",
                ).SerializeToString(),
            )
            return

        await session.cleanup()
        await session.publish_status(ModuleStatus.DISCONNECTED)
        await self.nc.publish(
            reply,
            session_dec.Status(
                session_id=sess_id,
                instance_id=self.instance_id,
                status=ModuleStatus.DISCONNECTED,
            ).SerializeToString(),
        )
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

    def __init__(self, nc: NATS, instances: List[str]):
        self.nc = nc
        self.instances = instances
        # Store status updates by session_id -> module -> status
        self.session_statuses: Dict[str, Dict[str, ModuleStatus]] = {}

    async def _on_status(self, msg):
        """Callback for status updates - stores them for later checking."""
        try:
            st = session_dec.Status()
            st.ParseFromString(msg.data)

            # Extract session_id from subject: session.<id>.<module>.status
            parts = msg.subject.split(".")
            if len(parts) >= 4:
                sess_id = parts[1]

                # Initialize nested dict if needed
                if sess_id not in self.session_statuses:
                    self.session_statuses[sess_id] = {}

                self.session_statuses[sess_id][st.instance_id] = st.status
                log.debug(
                    f"Stored status for session {sess_id}, instance {st.instance_id}: {st.status}"
                )
        except Exception as e:
            log.error(f"Failed to parse status message: {e}")

    # ---- public API ------------------------------------------------------
    async def start_session(
        self, sess_id: str, configs: Dict[str, bytes], *, timeout: float = 3.0
    ) -> None:
        """Spin‑up *all* modules; raise if any fails."""

        # Subscribe to status updates BEFORE sending any commands
        status_subj = f"session.{sess_id}.*.status"
        status_sub = await self.nc.subscribe(status_subj, cb=self._on_status)  # type: ignore[arg-type]
        log.debug(f"Subscribed to {status_subj}")

        try:
            # 1) Send Init commands in parallel and wait for INITIALIZING / FAILED replies.
            init_tasks: Dict[str, "asyncio.Task[bytes]"] = {}
            for instance in self.instances:
                cmd_subj = f"session.{sess_id}.{instance}.cmd"
                cmd = session_dec.Command(
                    init=session_dec.Init(session_id=sess_id, config=configs[instance])
                )
                log.debug(f"Sending init command to {cmd_subj}")
                init_tasks[cmd_subj] = asyncio.create_task(
                    self.nc.request(cmd_subj, cmd.SerializeToString(), timeout=timeout)
                )

            # Gather first replies – they unblock the request‑reply wait.
            for instance, t in init_tasks.items():
                log.info(f"Starting {instance}")
                try:
                    msg = await t
                except asyncio.TimeoutError as te:  # noqa: PERF203 – keep explicit
                    raise RuntimeError(f"{instance} did not ACK in {timeout}s") from te
                except Exception as e:
                    log.error(f"Error waiting for reply from {instance}: {e}")
                    raise e

                log.debug(f"Received reply from {instance}, type: {type(msg)}")

                # Check if msg is bytes or a Message object
                if hasattr(msg, "data"):
                    data = msg.data
                else:
                    data = msg

                log.debug(f"Reply data from {instance}: {len(data)} bytes")
                try:
                    st = session_dec.Status()
                    st.ParseFromString(data)
                    if st.status == ModuleStatus.FAILED:
                        raise RuntimeError(
                            f"{instance} failed during init: {st.detail}"
                        )
                except Exception as e:
                    log.error(f"Failed to parse reply from {instance}: {e}")
                    log.error(f"Reply data (first 100 bytes): {data[:100]}")
                    raise

            # 2) Wait until every module reports RUNNING via the status updates
            await self._wait_for_running(sess_id)
            log.info("✅ Session %s READY", sess_id)

        finally:
            # Clean up subscription
            await status_sub.unsubscribe()

    async def stop_session(self, sess_id: str, *, timeout: float = 0.1) -> None:
        """Gracefully tear‑down all modules."""
        shutdown_tasks: Dict[str, "asyncio.Task[bytes]"] = {}
        for m in self.instances:
            log.info(f"Stopping {m}")
            subj = f"session.{sess_id}.{m}.cmd"
            cmd = session_dec.Command(shutdown=session_dec.Shutdown(session_id=sess_id))
            shutdown_tasks[m] = asyncio.create_task(
                self.nc.request(subj, cmd.SerializeToString(), timeout=timeout)
            )

        for m, t in shutdown_tasks.items():
            try:
                msg = await t
            except asyncio.TimeoutError as te:  # noqa: PERF203
                raise RuntimeError(f"{m} did not ACK shutdown in {timeout}s") from te

            if hasattr(msg, "data"):
                data = msg.data
            else:
                data = msg

            st = session_dec.Status()
            st.ParseFromString(data)
            if st.status != ModuleStatus.DISCONNECTED:
                raise RuntimeError(f"{m} returned unexpected state {st.status}")

        # Clean up status tracking
        self.session_statuses.pop(sess_id, None)
        log.info("🛑 Session %s fully disconnected", sess_id)

    # ---- internals -------------------------------------------------------
    async def _wait_for_running(self, sess_id: str) -> None:
        """Wait for all modules to report RUNNING status."""
        max_wait = 10.0  # Maximum time to wait
        check_interval = 0.1  # How often to check
        elapsed = 0.0

        while elapsed < max_wait:
            statuses = self.session_statuses.get(sess_id, {})

            # Check if all modules are RUNNING
            if len(statuses) == len(self.instances) and all(
                statuses.get(m) == ModuleStatus.RUNNING for m in self.instances
            ):
                log.info(f"All started modules are RUNNING")
                return

            # Check for any failures
            for m in self.instances:
                status = statuses.get(m)
                if status == ModuleStatus.FAILED:
                    raise RuntimeError(f"Module {m} failed during initialization")

            await asyncio.sleep(check_interval)
            elapsed += check_interval

        # Timeout - report which modules aren't ready
        statuses = self.session_statuses.get(sess_id, {})
        not_running = []
        for m in self.instances:
            status = statuses.get(m)
            if status != ModuleStatus.RUNNING:
                not_running.append(
                    f"{m}={status if status is not None else 'no-status'}"
                )
        raise RuntimeError(f"Timeout waiting for modules to be RUNNING: {not_running}")

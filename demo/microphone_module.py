"""
Microphone module for streaming audio from device to NATS.
Demonstrates using BaseModule and BaseSession from the base framework.

Requirements:
- NATS server must have JetStream enabled (use -js flag when starting nats-server)
- sounddevice package for audio capture
- Working microphone device

To run NATS with JetStream:
    nats-server -js -p 9090
"""

import asyncio
import json
import sys
import sounddevice as sd
import numpy as np
import time
import logging
from typing import Optional

from nats.aio.client import Client as NATS
from odin.nats.base import BaseSession, BaseModule, ModuleStatus
from odin.v1 import audio_pb2, common_pb2

log = logging.getLogger(__name__)

SAMPLE_RATE = 16_000  # Hz
CHUNK_SIZE = 1_600    # 100ms of audio at 16kHz


class MicrophoneSession(BaseSession):
    """Handles audio streaming for one session."""
    
    def __init__(self, session_id: str, config: bytes, nc: NATS, module_name: str):
        super().__init__(session_id, config, nc, module_name)
        self.stream = None
        self.streaming_task = None
        self._stop_event = asyncio.Event()
        self.js = None  # Will be set by the module
        
        # Build subject for this session
        self.audio_subject = f"audio.{session_id}.{module_name}.input"
        
        # Parse config if provided
        if config:
            try:
                self.config_dict = json.loads(config.decode())
                self.sample_rate = self.config_dict.get("sample_rate", SAMPLE_RATE)
                self.chunk_size = self.config_dict.get("chunk_size", CHUNK_SIZE)
            except Exception:
                self.sample_rate = SAMPLE_RATE
                self.chunk_size = CHUNK_SIZE
        else:
            self.sample_rate = SAMPLE_RATE
            self.chunk_size = CHUNK_SIZE

    async def initialize(self) -> None:
        """Start the microphone stream and audio publishing task."""
        try:
            log.info(f"Starting initialization for microphone session {self.session_id}")
            
            # Verify JetStream is available
            if not self.js:
                raise RuntimeError("JetStream context not available")
            
            # List available audio devices for debugging
            devices = sd.query_devices()
            log.info(f"Available audio devices: {devices}")
            
            # Get default input device info for debugging
            default_input = sd.default.device[0]
            log.info(f"Default input device index: {default_input}")
            if default_input is not None:
                log.info(f"Default input device: {devices[default_input]}")
            
            # Create the audio stream
            self.stream = sd.InputStream(
                samplerate=self.sample_rate,
                channels=1,
                blocksize=self.chunk_size,
                dtype="int32",
            )
            self.stream.start()
            log.info(f"Audio stream started successfully")
            
            # Start the streaming task
            self.streaming_task = asyncio.create_task(self._stream_audio())
            
            log.info(f"Microphone session {self.session_id} initialized, publishing to {self.audio_subject}")
            
            # Give streaming task a moment to start
            await asyncio.sleep(0.1)
            
            # Check if streaming task failed immediately
            if self.streaming_task.done():
                exc = self.streaming_task.exception()
                if exc:
                    raise exc
                    
        except Exception as e:
            log.error(f"Failed to initialize microphone session: {e}", exc_info=True)
            # Make sure to update status on failure
            await self.publish_status(ModuleStatus.FAILED, str(e))
            raise

    async def cleanup(self) -> None:
        """Stop streaming and clean up resources."""
        # Signal the streaming task to stop
        self._stop_event.set()
        
        # Wait for streaming task to complete
        if self.streaming_task:
            try:
                await asyncio.wait_for(self.streaming_task, timeout=2.0)
            except asyncio.TimeoutError:
                log.warning(f"Streaming task for session {self.session_id} did not stop gracefully")
                self.streaming_task.cancel()
        
        # Close the audio stream
        if self.stream:
            self.stream.stop()
            self.stream.close()
            
        # Send end-of-stream marker via regular NATS
        eos_subject = f"audio.{self.session_id}.{self.module_name}.eos"
        await self.nc.publish(eos_subject, b"EOS")
        
        log.info(f"Microphone session {self.session_id} cleaned up")

    async def _stream_audio(self) -> None:
        """Main loop for streaming audio to NATS JetStream."""
        
        while not self._stop_event.is_set():
            try:
                # Read audio data from microphone
                data, overflowed = self.stream.read(self.chunk_size)
                
                if overflowed:
                    log.warning(f"Audio overflow in session {self.session_id}")
                
                # Build protobuf message
                audio_msg = common_pb2.AudioData(
                    audio_data=data.tobytes(),
                    sample_rate=self.sample_rate,
                )
                
                chunk_msg = audio_pb2.AudioBufferMic(
                    audio=audio_msg,
                    client_id=self.session_id,
                )
                
                # Publish to JetStream with session-specific subject
                ack = await self.js.publish(self.audio_subject, chunk_msg.SerializeToString())
                # Optionally log the ack for debugging
                # log.debug(f"Published audio chunk, stream seq: {ack.seq}")
                
            except Exception as e:
                if not self._stop_event.is_set():
                    log.error(f"Error streaming audio: {e}")
                    await self.publish_status(ModuleStatus.FAILED, str(e))
                    break


class MicrophoneModule(BaseModule):
    """Module that manages microphone streaming sessions."""
    
    def __init__(self, nc: NATS, name: str, queue_group: Optional[str] = None):
        super().__init__(nc, name, queue_group)
        self.js = None
        self.stream_created = False
    
    async def start(self) -> None:
        """Start the module and create JetStream resources."""
        try:
            # First create JetStream context
            self.js = self.nc.jetstream()
            
            # Test if JetStream is available by trying to get account info
            try:
                await self.js.account_info()
            except Exception as e:
                if "jetstream not enabled" in str(e).lower():
                    raise RuntimeError(
                        "JetStream is not enabled on the NATS server. "
                        "Please start NATS with the -js flag: nats-server -js -p 9090"
                    )
                raise
            
            # Create the audio stream if it doesn't exist
            await self._create_audio_stream()
            
            # Then start the normal module subscription
            await super().start()
        except Exception as e:
            log.error(f"Failed to start microphone module: {e}")
            raise

    async def _create_audio_stream(self) -> None:
        """Create JetStream stream for audio data."""
        try:
            # Define stream configuration
            stream_config = {
                "name": "AUDIO",
                "subjects": ["audio.>"],  # Matches all audio.* subjects
                "retention": "limits",
                "max_msgs": 100000,
                "max_bytes": 1024 * 1024 * 1024,  # 1GB
                "max_age": 3600 * 24 * 7,  # 7 days
                "storage": "file",
                "num_replicas": 1,
                "discard": "old",  # Discard old messages when limits are reached
            }
            
            # Try to create the stream
            try:
                await self.js.add_stream(**stream_config)
                log.info(f"Created JetStream stream 'AUDIO' for audio data")
            except Exception as e:
                # Stream might already exist, try to get it
                if "stream name already in use" in str(e).lower():
                    stream = await self.js.stream_info("AUDIO")
                    log.info(f"JetStream stream 'AUDIO' already exists with {stream.state.messages} messages")
                else:
                    raise
                    
            self.stream_created = True
            
        except Exception as e:
            log.error(f"Failed to create JetStream audio stream: {e}")
            raise

    async def _on_command(self, msg):
        """Override to add debug logging."""
        log.info(f"Microphone module received command on subject: {msg.subject}")
        log.info(f"Command data length: {len(msg.data)} bytes")
        # Call parent implementation
        await super()._on_command(msg)
    
    async def create_session(self, sess_id: str, cfg: bytes) -> BaseSession:
        """Factory method to create a new MicrophoneSession."""
        log.info(f"Creating microphone session for {sess_id}")
        session = MicrophoneSession(sess_id, cfg, self.nc, self.name)
        session.js = self.js  # Pass JetStream context to session
        return session


# Example usage
async def main():
    """Standalone test of the microphone module."""
    # Configure logging for all modules
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        force=True  # Force reconfiguration of all loggers
    )
    
    # Ensure odin.nats.base logger is also at DEBUG level
    logging.getLogger('odin.nats.base').setLevel(logging.DEBUG)
    
    # Check command line arguments  
    nats_url = "nats://127.0.0.1:9090"
    if len(sys.argv) > 1:
        nats_url = sys.argv[1]
    
    log.info(f"Connecting to NATS at {nats_url}...")
    
    # Connect to NATS
    nc = NATS()
    await nc.connect(nats_url)
    
    # Create and start the module
    module = MicrophoneModule(nc, "microphone")
    await module.start()
    
    log.info("Microphone module started. Waiting for commands...")
    
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        log.info("Shutting down...")
    finally:
        await nc.drain()
        log.info("Disconnected from NATS")


if __name__ == "__main__":
    asyncio.run(main())
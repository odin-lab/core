"""
Microphone module for streaming audio from device to NATS.
Demonstrates using BaseModule and BaseSession from the base framework.
"""

import asyncio
import json
import sounddevice as sd
import numpy as np
import time
import logging

from nats.aio.client import Client as NATS
from odin.nats.base import BaseSession, BaseModule, ModuleStatus
from odin.v1 import audio_pb2, common_pb2

log = logging.getLogger(__name__)

SAMPLE_RATE = 16_000  # Hz
CHUNK_SIZE = 1_600    # 100ms of audio at 16kHz
AUDIO_SUBJECT = "audio.input.chunk"


class MicrophoneSession(BaseSession):
    """Handles audio streaming for one session."""
    
    def __init__(self, session_id: str, config: bytes, nc: NATS, module_name: str):
        super().__init__(session_id, config, nc, module_name)
        self.stream = None
        self.streaming_task = None
        self._stop_event = asyncio.Event()
        
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
            # Create the audio stream
            self.stream = sd.InputStream(
                samplerate=self.sample_rate,
                channels=1,
                blocksize=self.chunk_size,
                dtype="float32",
            )
            self.stream.start()
            
            # Start the streaming task
            self.streaming_task = asyncio.create_task(self._stream_audio())
            
            log.info(f"Microphone session {self.session_id} initialized")
        except Exception as e:
            log.error(f"Failed to initialize microphone session: {e}")
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
            
        # Send end-of-stream marker via JetStream
        js = self.nc.jetstream()
        await js.publish(AUDIO_SUBJECT, b"EOS:" + self.session_id.encode())
        
        log.info(f"Microphone session {self.session_id} cleaned up")

    async def _stream_audio(self) -> None:
        """Main loop for streaming audio to NATS."""
        js = self.nc.jetstream()
        
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
                
                session_msg = common_pb2.SessionInfo(
                    id=self.session_id,
                    timestamp=int(time.time() * 1000),  # epoch milliseconds
                )
                
                chunk_msg = audio_pb2.AudioBufferSession(
                    audio=audio_msg,
                    session=session_msg,
                )
                
                # Publish to JetStream
                await js.publish(AUDIO_SUBJECT, chunk_msg.SerializeToString())
                
            except Exception as e:
                if not self._stop_event.is_set():
                    log.error(f"Error streaming audio: {e}")
                    await self.publish_status(ModuleStatus.FAILED, str(e))
                    break


class MicrophoneModule(BaseModule):
    """Module that manages microphone streaming sessions."""
    
    async def create_session(self, sess_id: str, cfg: bytes) -> BaseSession:
        """Factory method to create a new MicrophoneSession."""
        return MicrophoneSession(sess_id, cfg, self.nc, self.name)


# Example usage
async def main():
    """Standalone test of the microphone module."""
    logging.basicConfig(level=logging.INFO)
    
    # Connect to NATS
    nc = NATS()
    await nc.connect("nats://127.0.0.1:9090")
    
    # Create and start the module
    module = MicrophoneModule(nc, "microphone")
    await module.start()
    
    log.info("Microphone module started. Waiting for commands...")
    
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        await nc.drain()


if __name__ == "__main__":
    asyncio.run(main()) 
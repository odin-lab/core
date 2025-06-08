"""
Recorder module for saving audio streams to WAV files.
Demonstrates using BaseModule and BaseSession from the base framework.
"""

import asyncio
import json
import wave
import time
import logging
from pathlib import Path
from typing import Dict, Optional

from nats.aio.client import Client as NATS
from odin.nats.base import BaseSession, BaseModule, ModuleStatus
from odin.v1 import audio_pb2, common_pb2

log = logging.getLogger(__name__)

AUDIO_SUBJECT = "audio.input.chunk"
DEFAULT_OUTPUT_DIR = "recordings"


class RecorderSession(BaseSession):
    """Handles audio recording for one session."""
    
    def __init__(self, session_id: str, config: bytes, nc: NATS, module_name: str):
        super().__init__(session_id, config, nc, module_name)
        self.buffer = bytearray()
        self.sample_rate = 16_000
        self.recording_task = None
        self.subscription = None
        
        # Parse config if provided
        if config:
            try:
                self.config_dict = json.loads(config.decode())
                self.output_dir = Path(self.config_dict.get("output_dir", DEFAULT_OUTPUT_DIR))
            except Exception:
                self.output_dir = Path(DEFAULT_OUTPUT_DIR)
        else:
            self.output_dir = Path(DEFAULT_OUTPUT_DIR)
            
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def initialize(self) -> None:
        """Start listening for audio chunks from this session."""
        try:
            # Subscribe to audio chunks via JetStream
            js = self.nc.jetstream()
            
            # Create a deliver subject specific to this session
            deliver_subject = f"_recorder.{self.session_id}"
            
            # Subscribe with a filter for this specific session
            self.subscription = await js.subscribe(
                AUDIO_SUBJECT,
                durable=f"recorder_{self.session_id}",
                deliver_subject=deliver_subject,
                cb=self._on_audio_chunk
            )
            
            log.info(f"Recorder session {self.session_id} initialized and listening")
        except Exception as e:
            log.error(f"Failed to initialize recorder session: {e}")
            raise

    async def cleanup(self) -> None:
        """Clean up resources and save any remaining audio."""
        # Unsubscribe from audio stream
        if self.subscription:
            await self.subscription.unsubscribe()
        
        # Save any remaining audio
        if len(self.buffer) > 0:
            await self._save_recording()
            
        log.info(f"Recorder session {self.session_id} cleaned up")

    async def _on_audio_chunk(self, msg):
        """Handle incoming audio chunks or EOS markers."""
        try:
            # Check for EOS marker
            if msg.data.startswith(b"EOS:"):
                _, sid = msg.data.split(b":", 1)
                sid = sid.decode()
                
                if sid == self.session_id:
                    # This is our EOS marker - save the recording
                    await self._save_recording()
                    log.info(f"Received EOS for session {self.session_id}, saving recording")
                
                # Acknowledge the message
                await msg.ack()
                return
            
            # Deserialize protobuf message
            chunk = audio_pb2.AudioBufferSession()
            chunk.ParseFromString(msg.data)
            
            # Check if this chunk is for our session
            if chunk.session and chunk.session.id == self.session_id:
                # Update sample rate if provided
                if chunk.audio.sample_rate:
                    self.sample_rate = chunk.audio.sample_rate
                
                # Append audio data to buffer
                self.buffer.extend(chunk.audio.audio_data)
                
                # Acknowledge the message
                await msg.ack()
            else:
                # Not our session - don't acknowledge so another recorder can process it
                pass
                
        except Exception as e:
            log.error(f"Error processing audio chunk: {e}")
            await self.publish_status(ModuleStatus.FAILED, str(e))

    async def _save_recording(self) -> None:
        """Save the buffered audio to a WAV file."""
        if len(self.buffer) == 0:
            log.warning(f"No audio data to save for session {self.session_id}")
            return
            
        timestamp = int(time.time())
        filename = self.output_dir / f"recording_{self.session_id}_{timestamp}.wav"
        
        try:
            with wave.open(str(filename), 'wb') as wf:
                wf.setnchannels(1)  # Mono audio
                wf.setsampwidth(4)  # 32-bit float audio
                wf.setframerate(self.sample_rate)
                wf.writeframes(self.buffer)
            
            log.info(f"💾 Saved recording to {filename} ({len(self.buffer)} bytes)")
            
            # Clear the buffer after saving
            self.buffer.clear()
            
        except Exception as e:
            log.error(f"Failed to save recording: {e}")
            raise


class RecorderModule(BaseModule):
    """Module that manages audio recording sessions."""
    
    async def create_session(self, sess_id: str, cfg: bytes) -> BaseSession:
        """Factory method to create a new RecorderSession."""
        return RecorderSession(sess_id, cfg, self.nc, self.name)


# Example usage
async def main():
    """Standalone test of the recorder module."""
    logging.basicConfig(level=logging.INFO)
    
    # Connect to NATS
    nc = NATS()
    await nc.connect("nats://127.0.0.1:9090")
    
    # Create and start the module
    module = RecorderModule(nc, "recorder")
    await module.start()
    
    log.info("Recorder module started. Waiting for commands...")
    
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        await nc.drain()


if __name__ == "__main__":
    asyncio.run(main()) 
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

DEFAULT_OUTPUT_DIR = "recordings"
DEFAULT_SOURCE_MODULE = "microphone"


class RecorderSession(BaseSession):
    """Handles audio recording for one session."""
    
    def __init__(self, session_id: str, config: bytes, nc: NATS, module_name: str):
        super().__init__(session_id, config, nc, module_name)
        self.buffer = bytearray()
        self.sample_rate = 16_000
        self.recording_task = None
        self.audio_subscription = None
        self.eos_subscription = None
        
        # Parse config if provided
        if config:
            try:
                self.config_dict = json.loads(config.decode())
                self.output_dir = Path(self.config_dict.get("output_dir", DEFAULT_OUTPUT_DIR))
                self.source_module = self.config_dict.get("source_module", DEFAULT_SOURCE_MODULE)
            except Exception:
                self.output_dir = Path(DEFAULT_OUTPUT_DIR)
                self.source_module = DEFAULT_SOURCE_MODULE
        else:
            self.output_dir = Path(DEFAULT_OUTPUT_DIR)
            self.source_module = DEFAULT_SOURCE_MODULE
            
        # Build subjects for this session - listen to configured source module
        self.audio_subject = f"audio.{session_id}.{self.source_module}.input"
        self.eos_subject = f"audio.{session_id}.{self.source_module}.eos"
            
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def initialize(self) -> None:
        """Start listening for audio chunks from this session."""
        try:
            # Subscribe to audio chunks via JetStream
            js = self.nc.jetstream()
            
            # Subscribe to audio input from configured source module for this session
            self.audio_subscription = await js.subscribe(
                self.audio_subject,
                durable=f"recorder_{self.session_id}_audio",
                cb=self._on_audio_chunk
            )
            
            # Subscribe to EOS markers from configured source module for this session
            self.eos_subscription = await js.subscribe(
                self.eos_subject,
                durable=f"recorder_{self.session_id}_eos",
                cb=self._on_eos
            )
            
            log.info(f"Recorder session {self.session_id} initialized, listening to '{self.source_module}' module on {self.audio_subject}")
        except Exception as e:
            log.error(f"Failed to initialize recorder session: {e}")
            raise

    async def cleanup(self) -> None:
        """Clean up resources and save any remaining audio."""
        # Unsubscribe from audio streams
        if self.audio_subscription:
            await self.audio_subscription.unsubscribe()
        if self.eos_subscription:
            await self.eos_subscription.unsubscribe()
        
        # Save any remaining audio
        if len(self.buffer) > 0:
            await self._save_recording()
            
        log.info(f"Recorder session {self.session_id} cleaned up")

    async def _on_audio_chunk(self, msg):
        """Handle incoming audio chunks."""
        try:
            # Deserialize protobuf message
            chunk = audio_pb2.AudioBufferMic()
            chunk.ParseFromString(msg.data)
            
            # Update sample rate if provided
            if chunk.audio.sample_rate:
                self.sample_rate = chunk.audio.sample_rate
            
            # Append audio data to buffer
            self.buffer.extend(chunk.audio.audio_data)
            
            # Acknowledge the message
            await msg.ack()
                
        except Exception as e:
            log.error(f"Error processing audio chunk: {e}")
            await self.publish_status(ModuleStatus.FAILED, str(e))

    async def _on_eos(self, msg):
        """Handle end-of-stream markers."""
        try:
            # Save the recording
            await self._save_recording()
            log.info(f"Saved recording for session {self.session_id} after EOS from {self.source_module}")
            
            # Acknowledge the message
            await msg.ack()
            
        except Exception as e:
            log.error(f"Error processing EOS: {e}")
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
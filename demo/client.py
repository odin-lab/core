import asyncio, sounddevice as sd, numpy as np
import time, uuid

from nats.aio.client import Client as NATS
from odin.v1 import audio_pb2, common_pb2

SAMPLE_RATE = 16_000  # Hz
CHUNK = 1_600  # 100 ms of audio
SUBJECT = "audio.input.chunk"  # Matches the nats_subject option in audio.proto

# A unique session id for this client run
SESSION_ID = str(uuid.uuid4())


async def main():
    nc = NATS()
    await nc.connect("nats://127.0.0.1:4222")
    print("🎤  Streaming mic → NATS …  (Ctrl-C to stop)")

    try:
        with sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=1,
            blocksize=CHUNK,
            dtype="int16",
        ) as stream:
            while True:
                data, _ = stream.read(CHUNK)  # ndarray[int16]

                # Build the protobuf message
                audio_msg = common_pb2.AudioData(
                    audio_data=data.tobytes(),
                    sample_rate=SAMPLE_RATE,
                )
                session_msg = common_pb2.SessionInfo(
                    session_id=SESSION_ID,
                    timestamp=int(time.time() * 1000),  # epoch-ms
                )
                chunk_msg = audio_pb2.AudioInputChunk(
                    audio=audio_msg,
                    session=session_msg,
                )

                await nc.publish(SUBJECT, chunk_msg.SerializeToString())
    except KeyboardInterrupt:
        pass
    finally:
        # Tell the server we're finished (simple sentinel)
        await nc.publish(SUBJECT, b"EOS:" + SESSION_ID.encode())
        await nc.drain()
        print("✅  Client closed.")


if __name__ == "__main__":
    asyncio.run(main())

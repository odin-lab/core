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
    # Establish NATS connection and JetStream context
    nc = NATS()
    await nc.connect("nats://127.0.0.1:9090")

    # JetStream context (provides persistence & at-least-once semantics)
    js = nc.jetstream()
    print("🎤  Streaming mic → NATS …  (Ctrl-C to stop)")

    try:
        with sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=1,
            blocksize=CHUNK,
            dtype="float32",
        ) as stream:
            while True:
                data, _ = stream.read(CHUNK)  # ndarray[int32]

                # Build the protobuf message
                audio_msg = common_pb2.AudioData(
                    audio_data=data.tobytes(),
                    sample_rate=SAMPLE_RATE,
                )
                session_msg = common_pb2.SessionInfo(
                    id=SESSION_ID,
                    timestamp=int(time.time() * 1000),  # epoch-ms
                )
                chunk_msg = audio_pb2.AudioBufferSession(
                    audio=audio_msg,
                    session=session_msg,
                )

                # Publish through JetStream so the data is persisted
                await js.publish(SUBJECT, chunk_msg.SerializeToString())
    except KeyboardInterrupt:
        pass
    finally:
        # Notify listeners that this session has finished using JetStream as well
        await js.publish(SUBJECT, b"EOS:" + SESSION_ID.encode())
        await nc.drain()
        print("✅  Client closed.")


if __name__ == "__main__":
    asyncio.run(main())

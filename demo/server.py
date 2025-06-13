from pathlib import Path
import pickle
import asyncio, time, wave
import os, sys

# Make generated protobufs importable (../../proto/gen/python)
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "proto", "gen", "python"))

from nats.aio.client import Client as NATS
from odin.v1 import audio_pb2, common_pb2

SAMPLE_RATE = 16_000
SUBJECT = "audio.input.chunk"


def save_wav(pcm, sr, filename):
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(4)  # 16-bit PCM
        wf.setframerate(sr)
        wf.writeframes(pcm)


async def main():
    # Establish NATS connection and JetStream context
    nc = NATS()
    await nc.connect("nats://127.0.0.1:9090")

    js = nc.jetstream()
    print("📡  Listening on", SUBJECT, "via JetStream")

    # buffer = bytearray()
    buffer = {}
    sample_rates = {}

    async def on_msg(msg):
        nonlocal buffer, sample_rates
        if msg.data.startswith(b"EOS:"):
            # Client finished → dump WAV
            _, sid = msg.data.split(b":", 1)
            sid = sid.decode()

            pcm = buffer.pop(sid, None)
            sr = sample_rates.pop(sid, SAMPLE_RATE)

            filename = f"recording_{sid}_{int(time.time())}.wav"
            save_wav(pcm, sr, filename)
            print("💾  Saved", filename)

        else:
            # Deserialize protobuf message
            chunk = audio_pb2.AudioBufferSession()
            chunk.ParseFromString(msg.data)

            # # store as pickly
            # path = Path(".recordings")
            # path.mkdir(parents=True, exist_ok=True)
            # with open(
            #     path / f"recording_{chunk.client_id}_{int(time.time())}.pkl", "wb"
            # ) as f:
            #     pickle.dump(chunk, f)
            # return

            sid = chunk.session.id if chunk.session else None
            if not sid:
                print("Warning: Received chunk without session ID")
                return

            if sid not in buffer:
                buffer[sid] = bytearray()
                sample_rates[sid] = chunk.audio.sample_rate or SAMPLE_RATE

            buffer[sid].extend(chunk.audio.audio_data)

            # Ack message so JetStream knows we've processed it
            await msg.ack()

    # Subscribe via JetStream with a durable consumer so we can resume after restarts
    await js.subscribe(SUBJECT, durable="audio_recorder", cb=on_msg)

    try:
        while True:
            await asyncio.sleep(3600)  # keep the process alive
    finally:
        await nc.drain()


if __name__ == "__main__":
    asyncio.run(main())

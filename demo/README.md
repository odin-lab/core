INSTALL: brew install nats-io/nats-tools/nats-server
RUN: nats-server -js


Server needs to:


- receive audio from client (async def on_msg(msg))
- check for EOS/END_OF_AUDIO (some signal to say it is over)
- check max. number users?
- initialize new client (either send back message SERVER_READY or ERROR)

WhisperLive:
- messages should contain (session id, status/type, message)
    - WhisperLive Messager:
        - wrong model size "uid": self.client_uid, "status": "ERROR", "message": f"Invalid model size"
        - language type detection "uid": self.client_uid, "language": self.language, "language_prob": info.language_probability
        - failed to load model "uid": self.client_uid, "status": "ERROR", "message": f"Failed to load model: {str(self.model_size_or_path)}"
        - server ready "uid": self.client_uid, "message": self.SERVER_READY, "backend": "faster_whisper"
        - server full "uid": options["uid"], "status": "WAIT", "message": wait_time
        - unsupported warning: "uid": self.client_uid, "status": "WARNING", "message": "TensorRT-LLM not supported on Server yet. " "Reverting to available backend: 'faster_whisper'"
        - segments "uid": self.client_uid, "segments": segments,
        -  disconnected (stopped thread) "uid": self.client_uid, "message": self.DISCONNECT (timeout)
    - so general types:
        - status updates - ERROR (wrong arguments/ failed to load) / WARNING (argument not supported - fallback) / WAIT (server full) / READY (after init) <- this is send as standard message
        - send language probability
        - send segments
        - disconnected
- for VAD get_speech_timestamps give us speech timestamps with actual audio

RealtimeTTS:


from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SessionInfo(_message.Message):
    __slots__ = ("id", "status", "language", "timestamp")
    ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    id: str
    status: str
    language: str
    timestamp: int
    def __init__(self, id: _Optional[str] = ..., status: _Optional[str] = ..., language: _Optional[str] = ..., timestamp: _Optional[int] = ...) -> None: ...

class AudioData(_message.Message):
    __slots__ = ("audio_data", "sample_rate")
    AUDIO_DATA_FIELD_NUMBER: _ClassVar[int]
    SAMPLE_RATE_FIELD_NUMBER: _ClassVar[int]
    audio_data: bytes
    sample_rate: int
    def __init__(self, audio_data: _Optional[bytes] = ..., sample_rate: _Optional[int] = ...) -> None: ...

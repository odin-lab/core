from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SessionInfo(_message.Message):
    __slots__ = ("session_id", "timestamp")
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    session_id: str
    timestamp: int
    def __init__(self, session_id: _Optional[str] = ..., timestamp: _Optional[int] = ...) -> None: ...

class AudioData(_message.Message):
    __slots__ = ("audio_data", "sample_rate")
    AUDIO_DATA_FIELD_NUMBER: _ClassVar[int]
    SAMPLE_RATE_FIELD_NUMBER: _ClassVar[int]
    audio_data: bytes
    sample_rate: int
    def __init__(self, audio_data: _Optional[bytes] = ..., sample_rate: _Optional[int] = ...) -> None: ...

class TranscriptionResult(_message.Message):
    __slots__ = ("text", "confidence")
    TEXT_FIELD_NUMBER: _ClassVar[int]
    CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    text: str
    confidence: float
    def __init__(self, text: _Optional[str] = ..., confidence: _Optional[float] = ...) -> None: ...

class ToolCall(_message.Message):
    __slots__ = ("function_name", "parameters")
    FUNCTION_NAME_FIELD_NUMBER: _ClassVar[int]
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    function_name: str
    parameters: str
    def __init__(self, function_name: _Optional[str] = ..., parameters: _Optional[str] = ...) -> None: ...

class ModuleInfo(_message.Message):
    __slots__ = ("module_name", "status")
    MODULE_NAME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    module_name: str
    status: str
    def __init__(self, module_name: _Optional[str] = ..., status: _Optional[str] = ...) -> None: ...

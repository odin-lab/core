from odin.v1 import common_pb2 as _common_pb2
from odin.v1 import options_pb2 as _options_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SpeechTranscriptionPartial(_message.Message):
    __slots__ = ("transcription", "session")
    TRANSCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SESSION_FIELD_NUMBER: _ClassVar[int]
    transcription: _common_pb2.TranscriptionResult
    session: _common_pb2.SessionInfo
    def __init__(self, transcription: _Optional[_Union[_common_pb2.TranscriptionResult, _Mapping]] = ..., session: _Optional[_Union[_common_pb2.SessionInfo, _Mapping]] = ...) -> None: ...

class SpeechTranscriptionFinal(_message.Message):
    __slots__ = ("transcription", "session")
    TRANSCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SESSION_FIELD_NUMBER: _ClassVar[int]
    transcription: _common_pb2.TranscriptionResult
    session: _common_pb2.SessionInfo
    def __init__(self, transcription: _Optional[_Union[_common_pb2.TranscriptionResult, _Mapping]] = ..., session: _Optional[_Union[_common_pb2.SessionInfo, _Mapping]] = ...) -> None: ...

class SpeechTurnDetected(_message.Message):
    __slots__ = ("is_speaking", "confidence", "session")
    IS_SPEAKING_FIELD_NUMBER: _ClassVar[int]
    CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    SESSION_FIELD_NUMBER: _ClassVar[int]
    is_speaking: bool
    confidence: float
    session: _common_pb2.SessionInfo
    def __init__(self, is_speaking: bool = ..., confidence: _Optional[float] = ..., session: _Optional[_Union[_common_pb2.SessionInfo, _Mapping]] = ...) -> None: ...

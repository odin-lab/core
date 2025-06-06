from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class TranscriptionResult(_message.Message):
    __slots__ = ("text", "confidence")
    TEXT_FIELD_NUMBER: _ClassVar[int]
    CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    text: _containers.RepeatedScalarFieldContainer[str]
    confidence: float
    def __init__(self, text: _Optional[_Iterable[str]] = ..., confidence: _Optional[float] = ...) -> None: ...

class TurnResult(_message.Message):
    __slots__ = ("text", "is_speaking")
    TEXT_FIELD_NUMBER: _ClassVar[int]
    IS_SPEAKING_FIELD_NUMBER: _ClassVar[int]
    text: _containers.RepeatedScalarFieldContainer[str]
    is_speaking: bool
    def __init__(self, text: _Optional[_Iterable[str]] = ..., is_speaking: bool = ...) -> None: ...

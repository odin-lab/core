from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class TranscriptionResult(_message.Message):
    __slots__ = ("text", "completed", "start", "end")
    TEXT_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    text: _containers.RepeatedScalarFieldContainer[str]
    completed: _containers.RepeatedScalarFieldContainer[bool]
    start: _containers.RepeatedScalarFieldContainer[float]
    end: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, text: _Optional[_Iterable[str]] = ..., completed: _Optional[_Iterable[bool]] = ..., start: _Optional[_Iterable[float]] = ..., end: _Optional[_Iterable[float]] = ...) -> None: ...

class TurnResult(_message.Message):
    __slots__ = ("text", "odins_turn")
    TEXT_FIELD_NUMBER: _ClassVar[int]
    ODINS_TURN_FIELD_NUMBER: _ClassVar[int]
    text: _containers.RepeatedScalarFieldContainer[str]
    odins_turn: bool
    def __init__(self, text: _Optional[_Iterable[str]] = ..., odins_turn: bool = ...) -> None: ...

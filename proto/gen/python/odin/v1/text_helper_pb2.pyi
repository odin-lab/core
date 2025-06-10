from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Segment(_message.Message):
    __slots__ = ("text", "completed", "start", "end")
    TEXT_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    text: str
    completed: bool
    start: float
    end: float
    def __init__(self, text: _Optional[str] = ..., completed: bool = ..., start: _Optional[float] = ..., end: _Optional[float] = ...) -> None: ...

class TurnResult(_message.Message):
    __slots__ = ("text", "odins_turn")
    TEXT_FIELD_NUMBER: _ClassVar[int]
    ODINS_TURN_FIELD_NUMBER: _ClassVar[int]
    text: _containers.RepeatedScalarFieldContainer[str]
    odins_turn: bool
    def __init__(self, text: _Optional[_Iterable[str]] = ..., odins_turn: bool = ...) -> None: ...

from odin.v1 import common_pb2 as _common_pb2
from odin.v1 import options_pb2 as _options_pb2
from odin.v1 import session_pb2 as _session_pb2
from odin.v1 import text_helper_pb2 as _text_helper_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class State(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    IDLE: _ClassVar[State]
    AWAKE: _ClassVar[State]
    THINKING: _ClassVar[State]
    SPEAKING: _ClassVar[State]
IDLE: State
AWAKE: State
THINKING: State
SPEAKING: State

class StateUpdate(_message.Message):
    __slots__ = ("state", "info")
    STATE_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    state: State
    info: _common_pb2.MessageInfo
    def __init__(self, state: _Optional[_Union[State, str]] = ..., info: _Optional[_Union[_common_pb2.MessageInfo, _Mapping]] = ...) -> None: ...

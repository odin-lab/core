from odin.v1 import common_pb2 as _common_pb2
from odin.v1 import options_pb2 as _options_pb2
from odin.v1 import session_pb2 as _session_pb2
from odin.v1 import text_helper_pb2 as _text_helper_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FlowType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LLM: _ClassVar[FlowType]
    SPEECH: _ClassVar[FlowType]
LLM: FlowType
SPEECH: FlowType

class Start(_message.Message):
    __slots__ = ("flow_type", "info")
    FLOW_TYPE_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    flow_type: FlowType
    info: _common_pb2.MessageInfo
    def __init__(self, flow_type: _Optional[_Union[FlowType, str]] = ..., info: _Optional[_Union[_common_pb2.MessageInfo, _Mapping]] = ...) -> None: ...

class Stop(_message.Message):
    __slots__ = ("flow_type", "info")
    FLOW_TYPE_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    flow_type: FlowType
    info: _common_pb2.MessageInfo
    def __init__(self, flow_type: _Optional[_Union[FlowType, str]] = ..., info: _Optional[_Union[_common_pb2.MessageInfo, _Mapping]] = ...) -> None: ...

class TurnDetected(_message.Message):
    __slots__ = ("segments", "text", "info")
    SEGMENTS_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    segments: _containers.RepeatedCompositeFieldContainer[_text_helper_pb2.Segment]
    text: str
    info: _common_pb2.MessageInfo
    def __init__(self, segments: _Optional[_Iterable[_Union[_text_helper_pb2.Segment, _Mapping]]] = ..., text: _Optional[str] = ..., info: _Optional[_Union[_common_pb2.MessageInfo, _Mapping]] = ...) -> None: ...

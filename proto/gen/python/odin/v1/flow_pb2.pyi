from odin.v1 import common_pb2 as _common_pb2
from odin.v1 import options_pb2 as _options_pb2
from odin.v1 import session_pb2 as _session_pb2
from odin.v1 import text_helper_pb2 as _text_helper_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TurnDetected(_message.Message):
    __slots__ = ("segments", "text", "info")
    SEGMENTS_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    segments: _containers.RepeatedCompositeFieldContainer[_text_helper_pb2.Segment]
    text: str
    info: _common_pb2.MessageInfo
    def __init__(self, segments: _Optional[_Iterable[_Union[_text_helper_pb2.Segment, _Mapping]]] = ..., text: _Optional[str] = ..., info: _Optional[_Union[_common_pb2.MessageInfo, _Mapping]] = ...) -> None: ...

class OdinStartSpeech(_message.Message):
    __slots__ = ("info",)
    INFO_FIELD_NUMBER: _ClassVar[int]
    info: _common_pb2.MessageInfo
    def __init__(self, info: _Optional[_Union[_common_pb2.MessageInfo, _Mapping]] = ...) -> None: ...

class OdinEndSpeech(_message.Message):
    __slots__ = ("info",)
    INFO_FIELD_NUMBER: _ClassVar[int]
    info: _common_pb2.MessageInfo
    def __init__(self, info: _Optional[_Union[_common_pb2.MessageInfo, _Mapping]] = ...) -> None: ...

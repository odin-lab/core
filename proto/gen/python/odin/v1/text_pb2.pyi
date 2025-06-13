from odin.v1 import common_pb2 as _common_pb2
from odin.v1 import options_pb2 as _options_pb2
from odin.v1 import text_helper_pb2 as _text_helper_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CompletionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    WORD: _ClassVar[CompletionType]
    SENTENCE: _ClassVar[CompletionType]
WORD: CompletionType
SENTENCE: CompletionType

class Transcription(_message.Message):
    __slots__ = ("segments", "info")
    SEGMENTS_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    segments: _containers.RepeatedCompositeFieldContainer[_text_helper_pb2.Segment]
    info: _common_pb2.MessageInfo
    def __init__(self, segments: _Optional[_Iterable[_Union[_text_helper_pb2.Segment, _Mapping]]] = ..., info: _Optional[_Union[_common_pb2.MessageInfo, _Mapping]] = ...) -> None: ...

class Completion(_message.Message):
    __slots__ = ("content", "type", "info")
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    content: str
    type: CompletionType
    info: _common_pb2.MessageInfo
    def __init__(self, content: _Optional[str] = ..., type: _Optional[_Union[CompletionType, str]] = ..., info: _Optional[_Union[_common_pb2.MessageInfo, _Mapping]] = ...) -> None: ...

from odin.v1 import common_pb2 as _common_pb2
from odin.v1 import options_pb2 as _options_pb2
from odin.v1 import text_helper_pb2 as _text_helper_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Transcription(_message.Message):
    __slots__ = ("segments", "session")
    SEGMENTS_FIELD_NUMBER: _ClassVar[int]
    SESSION_FIELD_NUMBER: _ClassVar[int]
    segments: _containers.RepeatedCompositeFieldContainer[_text_helper_pb2.Segment]
    session: _common_pb2.SessionInfo
    def __init__(self, segments: _Optional[_Iterable[_Union[_text_helper_pb2.Segment, _Mapping]]] = ..., session: _Optional[_Union[_common_pb2.SessionInfo, _Mapping]] = ...) -> None: ...

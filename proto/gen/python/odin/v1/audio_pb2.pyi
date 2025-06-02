from odin.v1 import common_pb2 as _common_pb2
from odin.v1 import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AudioInputChunk(_message.Message):
    __slots__ = ("audio", "session")
    AUDIO_FIELD_NUMBER: _ClassVar[int]
    SESSION_FIELD_NUMBER: _ClassVar[int]
    audio: _common_pb2.AudioData
    session: _common_pb2.SessionInfo
    def __init__(self, audio: _Optional[_Union[_common_pb2.AudioData, _Mapping]] = ..., session: _Optional[_Union[_common_pb2.SessionInfo, _Mapping]] = ...) -> None: ...

class AudioOutputSpeech(_message.Message):
    __slots__ = ("audio", "session")
    AUDIO_FIELD_NUMBER: _ClassVar[int]
    SESSION_FIELD_NUMBER: _ClassVar[int]
    audio: _common_pb2.AudioData
    session: _common_pb2.SessionInfo
    def __init__(self, audio: _Optional[_Union[_common_pb2.AudioData, _Mapping]] = ..., session: _Optional[_Union[_common_pb2.SessionInfo, _Mapping]] = ...) -> None: ...

class AudioOutputVisualization(_message.Message):
    __slots__ = ("audio_levels", "session")
    AUDIO_LEVELS_FIELD_NUMBER: _ClassVar[int]
    SESSION_FIELD_NUMBER: _ClassVar[int]
    audio_levels: _containers.RepeatedScalarFieldContainer[float]
    session: _common_pb2.SessionInfo
    def __init__(self, audio_levels: _Optional[_Iterable[float]] = ..., session: _Optional[_Union[_common_pb2.SessionInfo, _Mapping]] = ...) -> None: ...

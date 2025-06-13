from odin.v1 import common_pb2 as _common_pb2
from odin.v1 import options_pb2 as _options_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AudioBufferMic(_message.Message):
    __slots__ = ("audio", "client_id")
    AUDIO_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    audio: _common_pb2.AudioData
    client_id: str
    def __init__(self, audio: _Optional[_Union[_common_pb2.AudioData, _Mapping]] = ..., client_id: _Optional[str] = ...) -> None: ...

class AudioBufferSpeaker(_message.Message):
    __slots__ = ("audio", "info")
    AUDIO_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    audio: _common_pb2.AudioData
    info: _common_pb2.MessageInfo
    def __init__(self, audio: _Optional[_Union[_common_pb2.AudioData, _Mapping]] = ..., info: _Optional[_Union[_common_pb2.MessageInfo, _Mapping]] = ...) -> None: ...

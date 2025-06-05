from odin.v1 import common_pb2 as _common_pb2
from odin.v1 import options_pb2 as _options_pb2
from odin.v1 import text_helper_pb2 as _text_helper_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class STTranscript(_message.Message):
    __slots__ = ("transcription", "session")
    TRANSCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SESSION_FIELD_NUMBER: _ClassVar[int]
    transcription: _text_helper_pb2.TranscriptionResult
    session: _common_pb2.SessionInfo
    def __init__(self, transcription: _Optional[_Union[_text_helper_pb2.TranscriptionResult, _Mapping]] = ..., session: _Optional[_Union[_common_pb2.SessionInfo, _Mapping]] = ...) -> None: ...

class TextComplete(_message.Message):
    __slots__ = ("turn_result", "session")
    TURN_RESULT_FIELD_NUMBER: _ClassVar[int]
    SESSION_FIELD_NUMBER: _ClassVar[int]
    turn_result: _text_helper_pb2.TurnResult
    session: _common_pb2.SessionInfo
    def __init__(self, turn_result: _Optional[_Union[_text_helper_pb2.TurnResult, _Mapping]] = ..., session: _Optional[_Union[_common_pb2.SessionInfo, _Mapping]] = ...) -> None: ...

class TextOut(_message.Message):
    __slots__ = ("output_text", "session")
    OUTPUT_TEXT_FIELD_NUMBER: _ClassVar[int]
    SESSION_FIELD_NUMBER: _ClassVar[int]
    output_text: str
    session: _common_pb2.SessionInfo
    def __init__(self, output_text: _Optional[str] = ..., session: _Optional[_Union[_common_pb2.SessionInfo, _Mapping]] = ...) -> None: ...

class TextSpeech(_message.Message):
    __slots__ = ("output_text", "session")
    OUTPUT_TEXT_FIELD_NUMBER: _ClassVar[int]
    SESSION_FIELD_NUMBER: _ClassVar[int]
    output_text: str
    session: _common_pb2.SessionInfo
    def __init__(self, output_text: _Optional[str] = ..., session: _Optional[_Union[_common_pb2.SessionInfo, _Mapping]] = ...) -> None: ...

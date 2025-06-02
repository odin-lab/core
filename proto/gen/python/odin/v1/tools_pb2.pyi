from odin.v1 import common_pb2 as _common_pb2
from odin.v1 import options_pb2 as _options_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ToolsCallRequest(_message.Message):
    __slots__ = ("tool", "session")
    TOOL_FIELD_NUMBER: _ClassVar[int]
    SESSION_FIELD_NUMBER: _ClassVar[int]
    tool: _common_pb2.ToolCall
    session: _common_pb2.SessionInfo
    def __init__(self, tool: _Optional[_Union[_common_pb2.ToolCall, _Mapping]] = ..., session: _Optional[_Union[_common_pb2.SessionInfo, _Mapping]] = ...) -> None: ...

class ToolsCallResponse(_message.Message):
    __slots__ = ("result", "success", "error_msg", "session")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MSG_FIELD_NUMBER: _ClassVar[int]
    SESSION_FIELD_NUMBER: _ClassVar[int]
    result: str
    success: bool
    error_msg: str
    session: _common_pb2.SessionInfo
    def __init__(self, result: _Optional[str] = ..., success: bool = ..., error_msg: _Optional[str] = ..., session: _Optional[_Union[_common_pb2.SessionInfo, _Mapping]] = ...) -> None: ...

from odin.v1 import common_pb2 as _common_pb2
from odin.v1 import options_pb2 as _options_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SystemStatusModule(_message.Message):
    __slots__ = ("module", "session")
    MODULE_FIELD_NUMBER: _ClassVar[int]
    SESSION_FIELD_NUMBER: _ClassVar[int]
    module: _common_pb2.ModuleInfo
    session: _common_pb2.SessionInfo
    def __init__(self, module: _Optional[_Union[_common_pb2.ModuleInfo, _Mapping]] = ..., session: _Optional[_Union[_common_pb2.SessionInfo, _Mapping]] = ...) -> None: ...

class SystemErrorModule(_message.Message):
    __slots__ = ("error_code", "message", "module_name", "session")
    ERROR_CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    MODULE_NAME_FIELD_NUMBER: _ClassVar[int]
    SESSION_FIELD_NUMBER: _ClassVar[int]
    error_code: str
    message: str
    module_name: str
    session: _common_pb2.SessionInfo
    def __init__(self, error_code: _Optional[str] = ..., message: _Optional[str] = ..., module_name: _Optional[str] = ..., session: _Optional[_Union[_common_pb2.SessionInfo, _Mapping]] = ...) -> None: ...

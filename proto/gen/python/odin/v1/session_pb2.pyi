from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ModuleStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    INITIALIZING: _ClassVar[ModuleStatus]
    RUNNING: _ClassVar[ModuleStatus]
    FAILED: _ClassVar[ModuleStatus]
    DISCONNECTED: _ClassVar[ModuleStatus]
INITIALIZING: ModuleStatus
RUNNING: ModuleStatus
FAILED: ModuleStatus
DISCONNECTED: ModuleStatus

class Init(_message.Message):
    __slots__ = ("session_id", "config")
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    session_id: str
    config: bytes
    def __init__(self, session_id: _Optional[str] = ..., config: _Optional[bytes] = ...) -> None: ...

class Shutdown(_message.Message):
    __slots__ = ("session_id",)
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    session_id: str
    def __init__(self, session_id: _Optional[str] = ...) -> None: ...

class Command(_message.Message):
    __slots__ = ("init", "shutdown")
    INIT_FIELD_NUMBER: _ClassVar[int]
    SHUTDOWN_FIELD_NUMBER: _ClassVar[int]
    init: Init
    shutdown: Shutdown
    def __init__(self, init: _Optional[_Union[Init, _Mapping]] = ..., shutdown: _Optional[_Union[Shutdown, _Mapping]] = ...) -> None: ...

class Status(_message.Message):
    __slots__ = ("session_id", "module", "status", "detail")
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    MODULE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    DETAIL_FIELD_NUMBER: _ClassVar[int]
    session_id: str
    module: str
    status: ModuleStatus
    detail: str
    def __init__(self, session_id: _Optional[str] = ..., module: _Optional[str] = ..., status: _Optional[_Union[ModuleStatus, str]] = ..., detail: _Optional[str] = ...) -> None: ...

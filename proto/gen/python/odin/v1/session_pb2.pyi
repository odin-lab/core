from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ModuleStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    INITIALIZING: _ClassVar[ModuleStatus]
    RUNNING: _ClassVar[ModuleStatus]
    FAILED: _ClassVar[ModuleStatus]
    DISCONNECTED: _ClassVar[ModuleStatus]

class ModuleType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STT: _ClassVar[ModuleType]
    TTS: _ClassVar[ModuleType]
    AGENT: _ClassVar[ModuleType]
    TURN: _ClassVar[ModuleType]
    RECORDER: _ClassVar[ModuleType]
INITIALIZING: ModuleStatus
RUNNING: ModuleStatus
FAILED: ModuleStatus
DISCONNECTED: ModuleStatus
STT: ModuleType
TTS: ModuleType
AGENT: ModuleType
TURN: ModuleType
RECORDER: ModuleType

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
    __slots__ = ("session_id", "instance_id", "status", "detail")
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    DETAIL_FIELD_NUMBER: _ClassVar[int]
    session_id: str
    instance_id: str
    status: ModuleStatus
    detail: str
    def __init__(self, session_id: _Optional[str] = ..., instance_id: _Optional[str] = ..., status: _Optional[_Union[ModuleStatus, str]] = ..., detail: _Optional[str] = ...) -> None: ...

class ModuleBootup(_message.Message):
    __slots__ = ("type", "name", "instance_id", "started_at", "version", "host", "config_schema")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    STARTED_AT_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    HOST_FIELD_NUMBER: _ClassVar[int]
    CONFIG_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    type: ModuleType
    name: str
    instance_id: str
    started_at: int
    version: str
    host: str
    config_schema: str
    def __init__(self, type: _Optional[_Union[ModuleType, str]] = ..., name: _Optional[str] = ..., instance_id: _Optional[str] = ..., started_at: _Optional[int] = ..., version: _Optional[str] = ..., host: _Optional[str] = ..., config_schema: _Optional[str] = ...) -> None: ...

class ModuleHeartbeat(_message.Message):
    __slots__ = ("instance_id", "timestamp", "status", "active_sessions")
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_SESSIONS_FIELD_NUMBER: _ClassVar[int]
    instance_id: str
    timestamp: int
    status: ModuleStatus
    active_sessions: int
    def __init__(self, instance_id: _Optional[str] = ..., timestamp: _Optional[int] = ..., status: _Optional[_Union[ModuleStatus, str]] = ..., active_sessions: _Optional[int] = ...) -> None: ...

class ModuleRegistry(_message.Message):
    __slots__ = ("modules", "last_updated")
    MODULES_FIELD_NUMBER: _ClassVar[int]
    LAST_UPDATED_FIELD_NUMBER: _ClassVar[int]
    modules: _containers.RepeatedCompositeFieldContainer[ModuleBootup]
    last_updated: int
    def __init__(self, modules: _Optional[_Iterable[_Union[ModuleBootup, _Mapping]]] = ..., last_updated: _Optional[int] = ...) -> None: ...

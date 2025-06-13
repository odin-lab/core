// @generated by protoc-gen-es v2.5.2 with parameter "target=ts,import_extension=none"
// @generated from file odin/v1/session.proto (package odin.v1, syntax proto3)
/* eslint-disable */

import type { GenEnum, GenFile, GenMessage } from "@bufbuild/protobuf/codegenv2";
import { enumDesc, fileDesc, messageDesc } from "@bufbuild/protobuf/codegenv2";
import type { Message } from "@bufbuild/protobuf";

/**
 * Describes the file odin/v1/session.proto.
 */
export const file_odin_v1_session: GenFile = /*@__PURE__*/
  fileDesc("ChVvZGluL3YxL3Nlc3Npb24ucHJvdG8SB29kaW4udjEiKgoESW5pdBISCgpzZXNzaW9uX2lkGAEgASgJEg4KBmNvbmZpZxgCIAEoDCIeCghTaHV0ZG93bhISCgpzZXNzaW9uX2lkGAEgASgJIlYKB0NvbW1hbmQSHQoEaW5pdBgBIAEoCzINLm9kaW4udjEuSW5pdEgAEiUKCHNodXRkb3duGAIgASgLMhEub2Rpbi52MS5TaHV0ZG93bkgAQgUKA2NtZCJoCgZTdGF0dXMSEgoKc2Vzc2lvbl9pZBgBIAEoCRITCgtpbnN0YW5jZV9pZBgCIAEoCRIlCgZzdGF0dXMYAyABKA4yFS5vZGluLnYxLk1vZHVsZVN0YXR1cxIOCgZkZXRhaWwYBCABKAkingEKDE1vZHVsZUJvb3R1cBIhCgR0eXBlGAEgASgOMhMub2Rpbi52MS5Nb2R1bGVUeXBlEgwKBG5hbWUYAiABKAkSEwoLaW5zdGFuY2VfaWQYAyABKAkSEgoKc3RhcnRlZF9hdBgEIAEoAxIPCgd2ZXJzaW9uGAUgASgJEgwKBGhvc3QYBiABKAkSFQoNY29uZmlnX3NjaGVtYRgHIAEoCSJ5Cg9Nb2R1bGVIZWFydGJlYXQSEwoLaW5zdGFuY2VfaWQYAiABKAkSEQoJdGltZXN0YW1wGAMgASgDEiUKBnN0YXR1cxgEIAEoDjIVLm9kaW4udjEuTW9kdWxlU3RhdHVzEhcKD2FjdGl2ZV9zZXNzaW9ucxgFIAEoBSJOCg5Nb2R1bGVSZWdpc3RyeRImCgdtb2R1bGVzGAEgAygLMhUub2Rpbi52MS5Nb2R1bGVCb290dXASFAoMbGFzdF91cGRhdGVkGAIgASgDKksKDE1vZHVsZVN0YXR1cxIQCgxJTklUSUFMSVpJTkcQABILCgdSVU5OSU5HEAESCgoGRkFJTEVEEAISEAoMRElTQ09OTkVDVEVEEAMqMwoKTW9kdWxlVHlwZRIHCgNTVFQQABIHCgNUVFMQARIJCgVBR0VOVBACEggKBFRVUk4QA0JYCgtjb20ub2Rpbi52MUIMU2Vzc2lvblByb3RvUAGiAgNPWFiqAgdPZGluLlYxygIHT2RpblxWMeICE09kaW5cVjFcR1BCTWV0YWRhdGHqAghPZGluOjpWMWIGcHJvdG8z");

/**
 * @generated from message odin.v1.Init
 */
export type Init = Message<"odin.v1.Init"> & {
  /**
   * @generated from field: string session_id = 1;
   */
  sessionId: string;

  /**
   * @generated from field: bytes config = 2;
   */
  config: Uint8Array;
};

/**
 * Describes the message odin.v1.Init.
 * Use `create(InitSchema)` to create a new message.
 */
export const InitSchema: GenMessage<Init> = /*@__PURE__*/
  messageDesc(file_odin_v1_session, 0);

/**
 * @generated from message odin.v1.Shutdown
 */
export type Shutdown = Message<"odin.v1.Shutdown"> & {
  /**
   * @generated from field: string session_id = 1;
   */
  sessionId: string;
};

/**
 * Describes the message odin.v1.Shutdown.
 * Use `create(ShutdownSchema)` to create a new message.
 */
export const ShutdownSchema: GenMessage<Shutdown> = /*@__PURE__*/
  messageDesc(file_odin_v1_session, 1);

/**
 * @generated from message odin.v1.Command
 */
export type Command = Message<"odin.v1.Command"> & {
  /**
   * @generated from oneof odin.v1.Command.cmd
   */
  cmd: {
    /**
     * @generated from field: odin.v1.Init init = 1;
     */
    value: Init;
    case: "init";
  } | {
    /**
     * @generated from field: odin.v1.Shutdown shutdown = 2;
     */
    value: Shutdown;
    case: "shutdown";
  } | { case: undefined; value?: undefined };
};

/**
 * Describes the message odin.v1.Command.
 * Use `create(CommandSchema)` to create a new message.
 */
export const CommandSchema: GenMessage<Command> = /*@__PURE__*/
  messageDesc(file_odin_v1_session, 2);

/**
 * @generated from message odin.v1.Status
 */
export type Status = Message<"odin.v1.Status"> & {
  /**
   * @generated from field: string session_id = 1;
   */
  sessionId: string;

  /**
   * @generated from field: string instance_id = 2;
   */
  instanceId: string;

  /**
   * @generated from field: odin.v1.ModuleStatus status = 3;
   */
  status: ModuleStatus;

  /**
   * error text if FAILED
   *
   * @generated from field: string detail = 4;
   */
  detail: string;
};

/**
 * Describes the message odin.v1.Status.
 * Use `create(StatusSchema)` to create a new message.
 */
export const StatusSchema: GenMessage<Status> = /*@__PURE__*/
  messageDesc(file_odin_v1_session, 3);

/**
 * New messages for module bootup tracking
 *
 * @generated from message odin.v1.ModuleBootup
 */
export type ModuleBootup = Message<"odin.v1.ModuleBootup"> & {
  /**
   * @generated from field: odin.v1.ModuleType type = 1;
   */
  type: ModuleType;

  /**
   * name of the module (eg. whisper-live for stt)
   *
   * @generated from field: string name = 2;
   */
  name: string;

  /**
   * semi random id
   *
   * @generated from field: string instance_id = 3;
   */
  instanceId: string;

  /**
   * Unix timestamp
   *
   * @generated from field: int64 started_at = 4;
   */
  startedAt: bigint;

  /**
   * module version
   *
   * @generated from field: string version = 5;
   */
  version: string;

  /**
   * hostname/IP where module is running
   *
   * @generated from field: string host = 6;
   */
  host: string;

  /**
   * JSON schema for module config
   *
   * @generated from field: string config_schema = 7;
   */
  configSchema: string;
};

/**
 * Describes the message odin.v1.ModuleBootup.
 * Use `create(ModuleBootupSchema)` to create a new message.
 */
export const ModuleBootupSchema: GenMessage<ModuleBootup> = /*@__PURE__*/
  messageDesc(file_odin_v1_session, 4);

/**
 * @generated from message odin.v1.ModuleHeartbeat
 */
export type ModuleHeartbeat = Message<"odin.v1.ModuleHeartbeat"> & {
  /**
   * @generated from field: string instance_id = 2;
   */
  instanceId: string;

  /**
   * Unix timestamp of heartbeat
   *
   * @generated from field: int64 timestamp = 3;
   */
  timestamp: bigint;

  /**
   * @generated from field: odin.v1.ModuleStatus status = 4;
   */
  status: ModuleStatus;

  /**
   * number of active sessions
   *
   * @generated from field: int32 active_sessions = 5;
   */
  activeSessions: number;
};

/**
 * Describes the message odin.v1.ModuleHeartbeat.
 * Use `create(ModuleHeartbeatSchema)` to create a new message.
 */
export const ModuleHeartbeatSchema: GenMessage<ModuleHeartbeat> = /*@__PURE__*/
  messageDesc(file_odin_v1_session, 5);

/**
 * @generated from message odin.v1.ModuleRegistry
 */
export type ModuleRegistry = Message<"odin.v1.ModuleRegistry"> & {
  /**
   * @generated from field: repeated odin.v1.ModuleBootup modules = 1;
   */
  modules: ModuleBootup[];

  /**
   * @generated from field: int64 last_updated = 2;
   */
  lastUpdated: bigint;
};

/**
 * Describes the message odin.v1.ModuleRegistry.
 * Use `create(ModuleRegistrySchema)` to create a new message.
 */
export const ModuleRegistrySchema: GenMessage<ModuleRegistry> = /*@__PURE__*/
  messageDesc(file_odin_v1_session, 6);

/**
 * @generated from enum odin.v1.ModuleStatus
 */
export enum ModuleStatus {
  /**
   * @generated from enum value: INITIALIZING = 0;
   */
  INITIALIZING = 0,

  /**
   * @generated from enum value: RUNNING = 1;
   */
  RUNNING = 1,

  /**
   * @generated from enum value: FAILED = 2;
   */
  FAILED = 2,

  /**
   * @generated from enum value: DISCONNECTED = 3;
   */
  DISCONNECTED = 3,
}

/**
 * Describes the enum odin.v1.ModuleStatus.
 */
export const ModuleStatusSchema: GenEnum<ModuleStatus> = /*@__PURE__*/
  enumDesc(file_odin_v1_session, 0);

/**
 * @generated from enum odin.v1.ModuleType
 */
export enum ModuleType {
  /**
   * @generated from enum value: STT = 0;
   */
  STT = 0,

  /**
   * @generated from enum value: TTS = 1;
   */
  TTS = 1,

  /**
   * @generated from enum value: AGENT = 2;
   */
  AGENT = 2,

  /**
   * @generated from enum value: TURN = 3;
   */
  TURN = 3,
}

/**
 * Describes the enum odin.v1.ModuleType.
 */
export const ModuleTypeSchema: GenEnum<ModuleType> = /*@__PURE__*/
  enumDesc(file_odin_v1_session, 1);


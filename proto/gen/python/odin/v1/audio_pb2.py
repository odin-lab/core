# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: odin/v1/audio.proto
# Protobuf Python Version: 6.31.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    6,
    31,
    1,
    '',
    'odin/v1/audio.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from odin.v1 import common_pb2 as odin_dot_v1_dot_common__pb2
from odin.v1 import options_pb2 as odin_dot_v1_dot_options__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x13odin/v1/audio.proto\x12\x07odin.v1\x1a\x14odin/v1/common.proto\x1a\x15odin/v1/options.proto\"q\n\x0e\x41udioBufferMic\x12(\n\x05\x61udio\x18\x01 \x01(\x0b\x32\x12.odin.v1.AudioDataR\x05\x61udio\x12\x1b\n\tclient_id\x18\x02 \x01(\tR\x08\x63lientId:\x18\x8a\xb5\x18\x10\x61udio.buffer.mic\x90\xb5\x18\x01\"\x8c\x01\n\x12\x41udioBufferSpeaker\x12(\n\x05\x61udio\x18\x01 \x01(\x0b\x32\x12.odin.v1.AudioDataR\x05\x61udio\x12.\n\x07session\x18\x02 \x01(\x0b\x32\x14.odin.v1.SessionInfoR\x07session:\x1c\x8a\xb5\x18\x14\x61udio.buffer.speaker\x90\xb5\x18\x01\"\x88\x01\n\x12\x41udioBufferSession\x12(\n\x05\x61udio\x18\x01 \x01(\x0b\x32\x12.odin.v1.AudioDataR\x05\x61udio\x12.\n\x07session\x18\x02 \x01(\x0b\x32\x14.odin.v1.SessionInfoR\x07session:\x18\x8a\xb5\x18\x14\x61udio.buffer.sessionBV\n\x0b\x63om.odin.v1B\nAudioProtoP\x01\xa2\x02\x03OXX\xaa\x02\x07Odin.V1\xca\x02\x07Odin\\V1\xe2\x02\x13Odin\\V1\\GPBMetadata\xea\x02\x08Odin::V1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'odin.v1.audio_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\013com.odin.v1B\nAudioProtoP\001\242\002\003OXX\252\002\007Odin.V1\312\002\007Odin\\V1\342\002\023Odin\\V1\\GPBMetadata\352\002\010Odin::V1'
  _globals['_AUDIOBUFFERMIC']._loaded_options = None
  _globals['_AUDIOBUFFERMIC']._serialized_options = b'\212\265\030\020audio.buffer.mic\220\265\030\001'
  _globals['_AUDIOBUFFERSPEAKER']._loaded_options = None
  _globals['_AUDIOBUFFERSPEAKER']._serialized_options = b'\212\265\030\024audio.buffer.speaker\220\265\030\001'
  _globals['_AUDIOBUFFERSESSION']._loaded_options = None
  _globals['_AUDIOBUFFERSESSION']._serialized_options = b'\212\265\030\024audio.buffer.session'
  _globals['_AUDIOBUFFERMIC']._serialized_start=77
  _globals['_AUDIOBUFFERMIC']._serialized_end=190
  _globals['_AUDIOBUFFERSPEAKER']._serialized_start=193
  _globals['_AUDIOBUFFERSPEAKER']._serialized_end=333
  _globals['_AUDIOBUFFERSESSION']._serialized_start=336
  _globals['_AUDIOBUFFERSESSION']._serialized_end=472
# @@protoc_insertion_point(module_scope)

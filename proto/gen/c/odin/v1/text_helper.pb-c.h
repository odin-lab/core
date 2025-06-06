/* Generated by the protocol buffer compiler.  DO NOT EDIT! */
/* Generated from: odin/v1/text_helper.proto */

#ifndef PROTOBUF_C_odin_2fv1_2ftext_5fhelper_2eproto__INCLUDED
#define PROTOBUF_C_odin_2fv1_2ftext_5fhelper_2eproto__INCLUDED

#include <protobuf-c/protobuf-c.h>

PROTOBUF_C__BEGIN_DECLS

#if PROTOBUF_C_VERSION_NUMBER < 1003000
# error This file was generated by a newer version of protobuf-c which is incompatible with your libprotobuf-c headers. Please update your headers.
#elif 1005002 < PROTOBUF_C_MIN_COMPILER_VERSION
# error This file was generated by an older version of protobuf-c which is incompatible with your libprotobuf-c headers. Please regenerate this file with a newer version of protobuf-c.
#endif


typedef struct Odin__V1__TranscriptionResult Odin__V1__TranscriptionResult;
typedef struct Odin__V1__TurnResult Odin__V1__TurnResult;


/* --- enums --- */


/* --- messages --- */

/*
 * Speech transcription result with confidence
 */
struct  Odin__V1__TranscriptionResult
{
  ProtobufCMessage base;
  size_t n_text;
  char **text;
  size_t n_completed;
  protobuf_c_boolean *completed;
  size_t n_start;
  float *start;
  size_t n_end;
  float *end;
};
#define ODIN__V1__TRANSCRIPTION_RESULT__INIT \
 { PROTOBUF_C_MESSAGE_INIT (&odin__v1__transcription_result__descriptor) \
    , 0,NULL, 0,NULL, 0,NULL, 0,NULL }


/*
 * Turn information with role and content
 */
struct  Odin__V1__TurnResult
{
  ProtobufCMessage base;
  size_t n_text;
  char **text;
  protobuf_c_boolean odins_turn;
};
#define ODIN__V1__TURN_RESULT__INIT \
 { PROTOBUF_C_MESSAGE_INIT (&odin__v1__turn_result__descriptor) \
    , 0,NULL, 0 }


/* Odin__V1__TranscriptionResult methods */
void   odin__v1__transcription_result__init
                     (Odin__V1__TranscriptionResult         *message);
size_t odin__v1__transcription_result__get_packed_size
                     (const Odin__V1__TranscriptionResult   *message);
size_t odin__v1__transcription_result__pack
                     (const Odin__V1__TranscriptionResult   *message,
                      uint8_t             *out);
size_t odin__v1__transcription_result__pack_to_buffer
                     (const Odin__V1__TranscriptionResult   *message,
                      ProtobufCBuffer     *buffer);
Odin__V1__TranscriptionResult *
       odin__v1__transcription_result__unpack
                     (ProtobufCAllocator  *allocator,
                      size_t               len,
                      const uint8_t       *data);
void   odin__v1__transcription_result__free_unpacked
                     (Odin__V1__TranscriptionResult *message,
                      ProtobufCAllocator *allocator);
/* Odin__V1__TurnResult methods */
void   odin__v1__turn_result__init
                     (Odin__V1__TurnResult         *message);
size_t odin__v1__turn_result__get_packed_size
                     (const Odin__V1__TurnResult   *message);
size_t odin__v1__turn_result__pack
                     (const Odin__V1__TurnResult   *message,
                      uint8_t             *out);
size_t odin__v1__turn_result__pack_to_buffer
                     (const Odin__V1__TurnResult   *message,
                      ProtobufCBuffer     *buffer);
Odin__V1__TurnResult *
       odin__v1__turn_result__unpack
                     (ProtobufCAllocator  *allocator,
                      size_t               len,
                      const uint8_t       *data);
void   odin__v1__turn_result__free_unpacked
                     (Odin__V1__TurnResult *message,
                      ProtobufCAllocator *allocator);
/* --- per-message closures --- */

typedef void (*Odin__V1__TranscriptionResult_Closure)
                 (const Odin__V1__TranscriptionResult *message,
                  void *closure_data);
typedef void (*Odin__V1__TurnResult_Closure)
                 (const Odin__V1__TurnResult *message,
                  void *closure_data);

/* --- services --- */


/* --- descriptors --- */

extern const ProtobufCMessageDescriptor odin__v1__transcription_result__descriptor;
extern const ProtobufCMessageDescriptor odin__v1__turn_result__descriptor;

PROTOBUF_C__END_DECLS


#endif  /* PROTOBUF_C_odin_2fv1_2ftext_5fhelper_2eproto__INCLUDED */

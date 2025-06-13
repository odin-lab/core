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


typedef struct Odin__V1__Segment Odin__V1__Segment;


/* --- enums --- */


/* --- messages --- */

/*
 * Speech transcription result with confidence
 */
struct  Odin__V1__Segment
{
  ProtobufCMessage base;
  char *text;
  protobuf_c_boolean completed;
  float start;
  float end;
};
#define ODIN__V1__SEGMENT__INIT \
 { PROTOBUF_C_MESSAGE_INIT (&odin__v1__segment__descriptor) \
    , (char *)protobuf_c_empty_string, 0, 0, 0 }


/* Odin__V1__Segment methods */
void   odin__v1__segment__init
                     (Odin__V1__Segment         *message);
size_t odin__v1__segment__get_packed_size
                     (const Odin__V1__Segment   *message);
size_t odin__v1__segment__pack
                     (const Odin__V1__Segment   *message,
                      uint8_t             *out);
size_t odin__v1__segment__pack_to_buffer
                     (const Odin__V1__Segment   *message,
                      ProtobufCBuffer     *buffer);
Odin__V1__Segment *
       odin__v1__segment__unpack
                     (ProtobufCAllocator  *allocator,
                      size_t               len,
                      const uint8_t       *data);
void   odin__v1__segment__free_unpacked
                     (Odin__V1__Segment *message,
                      ProtobufCAllocator *allocator);
/* --- per-message closures --- */

typedef void (*Odin__V1__Segment_Closure)
                 (const Odin__V1__Segment *message,
                  void *closure_data);

/* --- services --- */


/* --- descriptors --- */

extern const ProtobufCMessageDescriptor odin__v1__segment__descriptor;

PROTOBUF_C__END_DECLS


#endif  /* PROTOBUF_C_odin_2fv1_2ftext_5fhelper_2eproto__INCLUDED */

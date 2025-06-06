// @generated by protoc-gen-es v2.5.2 with parameter "target=ts,import_extension=none"
// @generated from file odin/v1/text.proto (package odin.v1, syntax proto3)
/* eslint-disable */

import type { GenFile, GenMessage } from "@bufbuild/protobuf/codegenv2";
import { fileDesc, messageDesc } from "@bufbuild/protobuf/codegenv2";
import type { SessionInfo } from "./common_pb";
import { file_odin_v1_common } from "./common_pb";
import { file_odin_v1_options } from "./options_pb";
import type { TranscriptionResult, TurnResult } from "./text_helper_pb";
import { file_odin_v1_text_helper } from "./text_helper_pb";
import type { Message } from "@bufbuild/protobuf";

/**
 * Describes the file odin/v1/text.proto.
 */
export const file_odin_v1_text: GenFile = /*@__PURE__*/
  fileDesc("ChJvZGluL3YxL3RleHQucHJvdG8SB29kaW4udjEigQEKDFNUVHJhbnNjcmlwdBIzCg10cmFuc2NyaXB0aW9uGAEgASgLMhwub2Rpbi52MS5UcmFuc2NyaXB0aW9uUmVzdWx0EiUKB3Nlc3Npb24YAiABKAsyFC5vZGluLnYxLlNlc3Npb25JbmZvOhWKtRgNdGV4dC5zZWdtZW50c5C1GAEidgoMVGV4dENvbXBsZXRlEigKC3R1cm5fcmVzdWx0GAEgASgLMhMub2Rpbi52MS5UdXJuUmVzdWx0EiUKB3Nlc3Npb24YAiABKAsyFC5vZGluLnYxLlNlc3Npb25JbmZvOhWKtRgNdGV4dC5jb21wbGV0ZZC1GAEiVwoHVGV4dE91dBITCgtvdXRwdXRfdGV4dBgBIAEoCRIlCgdzZXNzaW9uGAMgASgLMhQub2Rpbi52MS5TZXNzaW9uSW5mbzoQirUYCHRleHQub3V0kLUYASJdCgpUZXh0U3BlZWNoEhMKC291dHB1dF90ZXh0GAEgASgJEiUKB3Nlc3Npb24YAiABKAsyFC5vZGluLnYxLlNlc3Npb25JbmZvOhOKtRgLdGV4dC5zcGVlY2iQtRgBQlUKC2NvbS5vZGluLnYxQglUZXh0UHJvdG9QAaICA09YWKoCB09kaW4uVjHKAgdPZGluXFYx4gITT2RpblxWMVxHUEJNZXRhZGF0YeoCCE9kaW46OlYxYgZwcm90bzM", [file_odin_v1_common, file_odin_v1_options, file_odin_v1_text_helper]);

/**
 * output STT
 *
 * @generated from message odin.v1.STTranscript
 */
export type STTranscript = Message<"odin.v1.STTranscript"> & {
  /**
   * @generated from field: odin.v1.TranscriptionResult transcription = 1;
   */
  transcription?: TranscriptionResult;

  /**
   * @generated from field: odin.v1.SessionInfo session = 2;
   */
  session?: SessionInfo;
};

/**
 * Describes the message odin.v1.STTranscript.
 * Use `create(STTranscriptSchema)` to create a new message.
 */
export const STTranscriptSchema: GenMessage<STTranscript> = /*@__PURE__*/
  messageDesc(file_odin_v1_text, 0);

/**
 * Text input for LLM processing
 *
 * @generated from message odin.v1.TextComplete
 */
export type TextComplete = Message<"odin.v1.TextComplete"> & {
  /**
   * @generated from field: odin.v1.TurnResult turn_result = 1;
   */
  turnResult?: TurnResult;

  /**
   * @generated from field: odin.v1.SessionInfo session = 2;
   */
  session?: SessionInfo;
};

/**
 * Describes the message odin.v1.TextComplete.
 * Use `create(TextCompleteSchema)` to create a new message.
 */
export const TextCompleteSchema: GenMessage<TextComplete> = /*@__PURE__*/
  messageDesc(file_odin_v1_text, 1);

/**
 * Generated text response from LLM
 *
 * @generated from message odin.v1.TextOut
 */
export type TextOut = Message<"odin.v1.TextOut"> & {
  /**
   * @generated from field: string output_text = 1;
   */
  outputText: string;

  /**
   * @generated from field: odin.v1.SessionInfo session = 3;
   */
  session?: SessionInfo;
};

/**
 * Describes the message odin.v1.TextOut.
 * Use `create(TextOutSchema)` to create a new message.
 */
export const TextOutSchema: GenMessage<TextOut> = /*@__PURE__*/
  messageDesc(file_odin_v1_text, 2);

/**
 * Checked output for TTS
 *
 * @generated from message odin.v1.TextSpeech
 */
export type TextSpeech = Message<"odin.v1.TextSpeech"> & {
  /**
   * @generated from field: string output_text = 1;
   */
  outputText: string;

  /**
   * @generated from field: odin.v1.SessionInfo session = 2;
   */
  session?: SessionInfo;
};

/**
 * Describes the message odin.v1.TextSpeech.
 * Use `create(TextSpeechSchema)` to create a new message.
 */
export const TextSpeechSchema: GenMessage<TextSpeech> = /*@__PURE__*/
  messageDesc(file_odin_v1_text, 3);


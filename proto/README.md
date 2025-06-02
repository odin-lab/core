# Odin Protobuf Definitions

This directory contains the Protocol Buffer definitions for the Odin system, organized by domain and with NATS subject information embedded in the message definitions.

## Directory Structure

```
proto/
├── buf.yaml             # Buf configuration for linting and breaking changes
├── buf.gen.yaml         # Code generation configuration
├── odin/
│   └── v1/              # Version 1 of the API
│       ├── options.proto   # Custom options for NATS subjects
│       ├── common.proto    # Common shared types
│       ├── audio.proto     # Audio processing messages
│       ├── speech.proto    # Speech recognition messages
│       ├── text.proto      # Text processing messages
│       ├── tools.proto     # Tool/function call messages
│       ├── session.proto   # Session management messages
│       └── system.proto    # System status and error messages
└── gen/                 # Generated code directory
    ├── python/          # Python generated code
    ├── typescript/      # TypeScript generated code
    ├── cpp/             # C++ generated code
    ├── validate/        # JSON schema validation files
    └── docs/            # Generated documentation
```

## NATS Subject Integration

Each message type that is published/subscribed over NATS has embedded subject information using custom protobuf options. This allows for type-safe subject handling and a single source of truth for message routing.

Example:

```protobuf
message AudioInputChunk {
  option (odin.v1.nats_subject) = "audio.input.chunk";
  option (odin.v1.nats_jetstream) = true;

  AudioData audio = 1;
  SessionInfo session = 2;
}
```

## Code Generation

To generate code for all supported languages:

```bash
cd proto
buf generate
```

## Language-Specific Helpers

### Python Example

```python
import odin.v1.audio_pb2 as audio_pb2
from google.protobuf.descriptor import FieldDescriptor

def get_nats_subject(message_class):
    """Extract NATS subject from protobuf message options"""
    options = message_class.DESCRIPTOR.GetOptions()
    if options.HasExtension(odin.v1.options_pb2.nats_subject):
        return options.Extensions[odin.v1.options_pb2.nats_subject]
    return None

# Usage
subject = get_nats_subject(audio_pb2.AudioInputChunk)  # Returns "audio.input.chunk"
```

### TypeScript Example

```typescript
import { AudioInputChunk } from "./gen/typescript/odin/v1/audio_pb";

// Custom decorator or utility to extract subject
function getNatsSubject(messageType: any): string | undefined {
  return messageType.options?.natsSubject;
}

const subject = getNatsSubject(AudioInputChunk); // Returns "audio.input.chunk"
```

## Style Guidelines

- Use PascalCase for message names
- Use snake_case for field names
- Group related messages in domain-specific proto files
- Use common message types for shared structures
- Include clear comments for all messages and fields
- Use versioned packages (v1, v2, etc.) for API evolution

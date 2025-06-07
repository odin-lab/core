# Odin Protocol Buffers

Generated Protocol Buffer definitions for the Odin project.

## Installation

Install with uv:

```bash
uv add ./proto/gen/python
```

Or install in development mode:

```bash
uv add -e ./proto/gen/python
```

## Usage

```python
from odin.v1 import audio_pb2, common_pb2

# Create protobuf messages
chunk = audio_pb2.AudioInputChunk()
# ... use the protobuf classes
```

## Generated Modules

- `audio_pb2` - Audio-related protobuf definitions
- `common_pb2` - Common shared protobuf definitions
- `options_pb2` - Options and configuration protobuf definitions
- `session_pb2` - Session management protobuf definitions
- `speech_pb2` - Speech processing protobuf definitions
- `system_pb2` - System-related protobuf definitions
- `text_pb2` - Text processing protobuf definitions
- `tools_pb2` - Tools and utilities protobuf definitions

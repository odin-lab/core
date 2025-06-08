# Audio Recording Demo

This demo showcases the Odin module framework by implementing a distributed audio recording system using NATS + JetStream.

## Overview

The demo consists of three main components:

1. **Microphone Module** (`microphone_module.py`) - Captures audio from the microphone and streams it to NATS
2. **Recorder Module** (`recorder_module.py`) - Listens for audio streams and saves them to WAV files
3. **Session Manager** (`demo_manager.py`) - Orchestrates the modules and provides an interactive CLI

This demonstrates the key concepts of the Odin framework:
- **BaseModule**: Workers that handle commands and manage sessions
- **BaseSession**: Individual session instances with lifecycle management
- **SessionManager**: Orchestration layer for coordinating multiple modules

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ Session Manager │────▶│   Microphone    │────▶│    Recorder     │
│  (demo_manager) │     │    Module       │     │    Module       │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                       │                       │
         │                       ▼                       ▼
         │              ┌─────────────────┐     ┌─────────────────┐
         └─────────────▶│   NATS/JS       │◀────│   NATS/JS       │
                        │   Message Bus   │     │   Message Bus   │
                        └─────────────────┘     └─────────────────┘
```

## Prerequisites

1. Install NATS Server:
   ```bash
   brew install nats-io/nats-tools/nats-server  # macOS
   # or see https://docs.nats.io/running-a-nats-service/introduction/installation
   ```

2. Install Python dependencies:
   ```bash
   uv sync  # if using uv
   # or
   pip install -r requirements.txt
   ```

## Running the Demo

### Method 1: Using tmux (Recommended)

The easiest way to run all components:

```bash
./run_demo.sh
```

This will start all three components in a tmux session with split panes.

### Method 2: Manual Start

1. Start NATS with JetStream:
   ```bash
   nats-server -js
   ```

2. In separate terminals, start each module:
   ```bash
   # Terminal 1
   python microphone_module.py

   # Terminal 2
   python recorder_module.py

   # Terminal 3
   python demo_manager.py
   ```

## Using the Demo

Once all components are running, the Session Manager provides an interactive CLI:

```
🎙️  Audio Recording Session Manager
========================================
Commands:
  start [name]  - Start a new recording session
  stop <id>     - Stop a session by ID
  list          - List active sessions
  quit          - Exit the application
========================================

> start Morning Meeting
Session ID: a1b2c3d4-e5f6-7890-abcd-ef1234567890

> list
Active sessions:
  - Morning Meeting (a1b2c3d4) (running for 15.2s)

> stop a1b2
🛑 Morning Meeting (a1b2c3d4) stopped (duration: 23.5s)
```

## How It Works

1. **Session Start**:
   - Session Manager sends `Init` commands to both modules
   - Microphone module starts capturing audio
   - Recorder module starts listening for audio chunks
   - Both modules report `RUNNING` status

2. **Audio Streaming**:
   - Microphone captures audio in chunks (100ms at 16kHz)
   - Audio is published to NATS JetStream as protobuf messages
   - Recorder buffers the audio chunks by session ID

3. **Session Stop**:
   - Session Manager sends `Shutdown` commands
   - Microphone stops capturing and sends an EOS (End-of-Stream) marker
   - Recorder saves the buffered audio to a WAV file
   - Both modules report `DISCONNECTED` status

## Output

Recordings are saved to the `recordings/` directory as WAV files:
```
recordings/
├── recording_a1b2c3d4-e5f6-7890-abcd-ef1234567890_1234567890.wav
└── recording_b2c3d4e5-f6a7-8901-bcde-f23456789012_1234567891.wav
```

## Extending the Demo

This demo provides a foundation for building more complex pipelines:

- Add an STT module that processes audio chunks in real-time
- Add a TTS module that generates speech from text
- Add an LLM module for conversational AI
- Add multiple microphone sources for multi-user support

## Troubleshooting

- **"Module did not ACK"**: Ensure the module is running before starting sessions
- **No audio captured**: Check microphone permissions and device selection
- **Files not saved**: Ensure the `recordings/` directory is writable

## Notes

- The demo uses JetStream for message persistence and at-least-once delivery
- Each session has a unique ID that's used for routing and correlation
- The framework handles module lifecycle, status reporting, and error handling
- Module configurations can be customized per session (sample rate, output directory, etc.)


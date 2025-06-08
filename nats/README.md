# odin-nats

NATS-based orchestration layer for Odin speech pipeline.

## Installation

This package depends on the `odin-proto` package from the adjacent `proto/gen/python` directory.

### Development Installation with uv

From your project root, add both packages as editable dependencies:
```bash
# Install both packages - order matters!
uv add --editable ./extern/core/proto/gen/python
uv add --editable ./extern/core/nats
```

### Development Installation with pip

```bash
# Install with dependencies
cd /path/to/extern/core/nats
pip install -e .
```

Note: If you get an error about `odin-proto` not being found, you may need to install it first:
```bash
cd /path/to/extern/core/proto/gen/python
pip install -e .
```

### Dependencies

Direct dependencies:
- `nats-py` - NATS async client

Peer dependencies (must be installed separately):
- `odin-proto` - Protocol buffer definitions (from `../proto/gen/python`)

## Usage

```python
from odin.nats import BaseSession, BaseModule, SessionManager, ModuleStatus

# Implement your own session class
class MySession(BaseSession):
    async def initialize(self):
        # Initialize your engine
        pass
    
    async def cleanup(self):
        # Clean up resources
        pass

# Implement your module
class MyModule(BaseModule):
    async def create_session(self, sess_id: str, cfg: bytes) -> BaseSession:
        return MySession(sess_id, cfg, self.nc, self.name)

# Use the SessionManager to orchestrate sessions
manager = SessionManager(nc, ["stt", "tts", "llm"])
await manager.start_session("session123", configs)
```

## Package Structure

```
odin/
├── __init__.py         # Namespace package
└── nats/
    ├── __init__.py     # Package exports
    └── base.py         # Core classes
```

## Key Components

- **BaseSession**: Abstract base class for module sessions
- **BaseModule**: Abstract base class for NATS queue workers
- **SessionManager**: Orchestration layer for managing multi-module sessions
- **ModuleStatus**: Enum for module states (INITIALIZING, RUNNING, FAILED, DISCONNECTED) 
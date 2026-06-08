# simplex-engine

Simplex Engine is a modern game engine written in Python, featuring an Entity-Component-System (ECS) architecture with integrated development tools.

We believe hardware performance will continue to improve in the future.
This project aims to deliver the best experience to our customers:
- Game players
- Game developers  
- Video creators

We believe a simplified engine (less code complexity, more functionality) will make game and video development faster, easier, and better.

**Current Focus**: Building a Minecraft-like voxel game engine with infinite procedural worlds, multiplayer support, and comprehensive development tools.

## Features

### Implemented
- **ECS Architecture**: Entity-Component-System with component filtering and event integration
- **OpenGL Voxel Rendering**: Chunk meshes via greedy/naive meshing, VBO upload, ECS draw path
- **Chunk Manager**: LRU-cached chunk storage with preload/unload APIs
- **First-Person Controls**: WASD + mouse look for Minecraft-like demos
- **Event-Driven Design**: Unified event system for cross-subsystem communication
- **Input System**: Pygame backend with keyboard/mouse (OpenGL renderer owns display in 3D mode)
- **2D Collision**: AABB collision for the ping-pong demo
- **Subsystem Scheduler**: Dependency-ordered engine initialization
- **Development Tools**: Debug overlay, logging, hot-reload hooks
- **MCP Server**: AI-native tools (tests, lint, world probe, docs resources)

### Planned
- **Block Interaction**: Place and break voxels
- **Cross-Chunk Meshing**: Neighbor-aware face culling
- **World Generation**: Noise terrain, biomes, and structures
- **Multiplayer**: Network architecture for multiplayer voxel worlds
- **Shader Pipeline**: Modern GL rendering (replace fixed-function path)

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/import1bones/simplex-engine.git
cd simplex-engine

# Install dependencies (using uv package manager)
uv sync
```

### Running the Minecraft-like Demo

```bash
# Interactive first-person voxel demo (3×3 chunks)
uv run python3 examples/minecraft-like/run_player.py

# Basic demo (single chunk, 5 frames)
uv run python3 examples/minecraft-like/run.py
```

Controls for `run_player.py`: **WASD** move, **mouse** look, **Space** up, **ESC** toggle mouse capture.

### Running the Ping-Pong Example

```bash
uv run python3 examples/ping_pong/run_simple.py
# Or the full-featured version:
uv run python3 examples/ping_pong/main_gui.py
```

Ping-pong controls: **W/S** or **arrow keys** for paddle, **F1–F4** debug keys when available.

### AI-native support (MCP)

Simplex includes an MCP server so Cursor and other AI clients can run tests, read docs, and probe the voxel world headlessly.

```bash
uv sync
uv run simplex-mcp --check  # smoke test (Cursor starts the server via .cursor/mcp.json)
```

Enable **simplex-engine** in Cursor MCP settings (config: `.cursor/mcp.json`). See [AGENTS.md](./AGENTS.md) and [docs/advanced/ai/README.md](./docs/advanced/ai/README.md).

## 📚 Documentation

Comprehensive documentation is available in the `docs/` directory:

- **[Getting Started](./docs/getting-started/)** - Installation, first project, and tutorials
- **[Core Concepts](./docs/core-concepts/)** - Architecture, ECS, events, and systems
- **[Examples & Tutorials](./docs/examples/)** - Complete games and step-by-step guides
- **[API Reference](./docs/api/)** - Complete API documentation
- **[Advanced Topics](./docs/advanced/)** - Performance, networking, and expert techniques
- **[Development Guide](./docs/development/)** - Contributing and extending the engine

### Quick Navigation

| I want to... | Go to... |
|---------------|----------|
| **Learn the basics** | [Getting Started Guide](./docs/getting-started/) |
| **Build my first game** | [Ping Pong Tutorial](./docs/examples/ping-pong.md) |
| **Understand ECS** | [Core Concepts](./docs/core-concepts/) |
| **Find API details** | [API Reference](./docs/api/) |
| **Optimize performance** | [Advanced Topics](./docs/advanced/) |
| **Contribute code** | [CONTRIBUTING.md](./CONTRIBUTING.md) · [AGENTS.md](./AGENTS.md) |
| **Pick a starter task** | [GOOD_FIRST_ISSUES.md](./GOOD_FIRST_ISSUES.md) |

## Architecture

### Core Systems

- **Engine**: Central game engine coordinator
- **ECS (Entity-Component-System)**: Manages game entities and their components
- **Event System**: Handles communication between systems
- **Renderer**: OpenGL backend (3D voxels) and SimpleRenderer (2D pygame)
- **Voxel / World**: Block palette, chunk storage, mesh generation, ChunkManager
- **Input System**: Pygame polling or OpenGL event forwarding to InputSystem
- **Player Controller**: First-person movement for voxel demos
- **Collision / Movement / Scoring**: 2D systems for ping-pong demo

### Event-Driven Communication

All systems communicate through a unified event system:

```python
# Emit events
engine.events.emit('input', input_event)
engine.events.emit('physics_collision', collision_data)

# Register event handlers
engine.events.register('score', handle_score_event)
```

### Input System Architecture

**2D (ping-pong):** Pygame events → SimpleRenderer → EventSystem → InputSystem → game logic

**3D (voxel):** Pygame events → OpenGLRenderer (before ECS update) → EventSystem → InputSystem / FirstPersonController

### Advantages

By using Python for all subsystems, this engine provides dynamic behavior when building game or video systems.
For example, when you write a command, you immediately see the result on your monitor. Once you confirm it works as intended, you can build for better performance.

Python offers a superior development interface, making development and debugging easier and faster.

## Examples

### Minecraft-like Voxel Demo

Demonstrates the current development focus:

- OpenGL rendering of ECS chunk meshes
- Greedy meshing for 16³ chunks
- ChunkManager with LRU caching
- First-person player controls (`run_player.py`)

### Ping-Pong Game

A complete 2D game demonstrating:

- Player vs AI gameplay
- Real-time input handling
- Collision detection between ball and paddles
- Scoring system with win conditions
- Debug overlay for development

### Creating Entities

```python
from simplex.ecs.ecs import Entity
from simplex.ecs.components import PositionComponent, VelocityComponent

# Create a player entity
player = Entity('player')
player.add_component(PositionComponent(100, 200, 0))
player.add_component(VelocityComponent(0, 0, 0))
engine.ecs.add_entity(player)
```

### System Integration

```python
from simplex.ecs.systems import InputSystem, MovementSystem

# Create and register systems
input_system = InputSystem(event_system=engine.events)
movement_system = MovementSystem(event_system=engine.events)

engine.ecs.add_system(input_system)
engine.ecs.add_system(movement_system)
```

## Development Tools

### Debug Features

- **Debug Overlay**: Real-time system information
- **Pause System**: Pause/resume game execution
- **Development Console**: Runtime debugging capabilities
- **Logging System**: Multi-level logging with configurable output

### Configuration

The engine uses TOML configuration files for settings:

```toml
[renderer]
backend = "opengl"
width = 800
height = 600
```

## Project Structure

```
simplex-engine/
├── simplex/
│   ├── engine.py              # Core engine coordinator
│   ├── ecs/                   # Entity-Component-System
│   ├── renderer/              # OpenGL + SimpleRenderer backends
│   ├── voxel/                 # Blocks, chunks, mesh generation
│   ├── world/                 # ChunkManager streaming
│   ├── scheduler/             # SubsystemManager
│   └── event/                 # Event system
├── examples/
│   ├── minecraft-like/        # Voxel demos (run.py, run_player.py)
│   └── ping_pong/             # 2D ping-pong example
├── tests/                     # Unit tests (pytest)
└── docs/                      # Documentation
```

## Contributing

1. Fork the repository
2. Create a feature branch from `main`
3. Make your changes
4. Run `uv run ruff check simplex/ tests/` and `uv run pytest tests/`
5. Submit a pull request (CI runs on push)

## Recent Updates

### OpenGL Voxel Backend (v0.0.2-dev)

- OpenGL renderer with VBO manager and ECS mesh rendering
- Voxel subsystem: chunks, greedy meshing, ChunkManager
- First-person player demo (`examples/minecraft-like/run_player.py`)
- GitHub Actions CI: `uv sync`, ruff, pytest

See [docs/todo/todo.md](./docs/todo/todo.md) for the full roadmap.

## License

MIT License — see [LICENSE](./LICENSE).

## Support

For issues, questions, or contributions, please visit the [GitHub repository](https://github.com/import1bones/simplex-engine).

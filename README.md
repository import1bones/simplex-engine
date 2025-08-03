# simplex-engine

Simplex Engine is a modern game engine written in Python, featuring an Entity-Component-System (ECS) architecture with integrated development tools.

We believe hardware performance will continue to improve in the future.
This project aims to deliver the best experience to our customers:
- Game players
- Game developers  
- Video creators

We believe a simplified engine (less code complexity, more functionality) will make game and video development faster, easier, and better.

## Features

- **ECS Architecture**: Entity-Component-System for clean, modular game logic
- **Event-Driven Design**: Unified event system for inter-system communication
- **Input System**: Responsive input handling with keyboard support (W/S/UP/DOWN)
- **Collision Detection**: AABB collision system with boundary checking
- **Rendering System**: Pygame-based renderer with debug overlay support
- **AI Systems**: Built-in AI movement and behavior systems
- **Development Tools**: Debug overlays, pause system, and real-time configuration
- **Scoring System**: Integrated scoring and game state management

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/import1bones/simplex-engine.git
cd simplex-engine

# Install dependencies (using uv package manager)
uv sync
```

### Running the Ping-Pong Example

```bash
# Set up Python path and run the game
PYTHONPATH=/path/to/simplex-engine python3 examples/ping_pong/test_simple.py

# Or run the full-featured version
PYTHONPATH=/path/to/simplex-engine python3 examples/ping_pong/main_gui.py
```

### Controls

- **W/S Keys**: Move player paddle up/down
- **UP/DOWN Arrow Keys**: Alternative paddle controls
- **F1-F4**: Debug functions (when available)
- **ESC**: Exit game

## Architecture

### Core Systems

- **Engine**: Central game engine coordinator
- **ECS (Entity-Component-System)**: Manages game entities and their components
- **Event System**: Handles communication between systems
- **Renderer**: Graphics rendering with pygame backend
- **Input System**: Processes keyboard input and forwards to game systems
- **Collision System**: Detects and handles entity collisions
- **Movement System**: Applies velocity to entity positions
- **Scoring System**: Manages game scoring and win conditions

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

The input system features a unified pipeline:
1. **Pygame Events** → captured by SimpleRenderer
2. **Event Translation** → pygame events converted to engine events
3. **Input System** → processes events and maintains input state
4. **Game Logic** → systems respond to input state changes

### Advantages

By using Python for all subsystems, this engine provides dynamic behavior when building game or video systems.
For example, when you write a command, you immediately see the result on your monitor. Once you confirm it works as intended, you can build for better performance.

Python offers a superior development interface, making development and debugging easier and faster.

## Examples

### Basic Ping-Pong Game

The engine includes a complete ping-pong game demonstrating:

- Player vs AI gameplay
- Real-time input handling
- Collision detection between ball and paddles
- Boundary collision handling
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
[engine]
debug_mode = true
target_fps = 60

[renderer]
width = 800
height = 600
```

## Project Structure

```
simplex-engine/
├── simplex/
│   ├── engine.py              # Core engine
│   ├── ecs/                   # Entity-Component-System
│   │   ├── ecs.py            # ECS implementation
│   │   ├── components.py     # Game components
│   │   └── systems.py        # Game systems
│   ├── renderer/              # Rendering system
│   │   └── simple_renderer.py
│   ├── utils/                 # Utilities
│   └── events/               # Event system
├── examples/
│   └── ping_pong/            # Ping-pong game example
└── docs/                     # Documentation
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with the ping-pong example
5. Submit a pull request

## Recent Updates

### Input System Fixes (Latest)

- Fixed input responsiveness issues where keys would only work once
- Implemented proper KEYUP/KEYDOWN event handling
- Unified input pipeline through SimpleRenderer
- Added comprehensive input state management
- Enhanced logging for input debugging

### Game Features

- Complete ping-pong game with AI opponent
- Enhanced collision detection with spin effects
- Scoring system with win conditions
- Real-time score display
- Smooth 60fps gameplay

## License

[License information to be added]

## Support

For issues, questions, or contributions, please visit the [GitHub repository](https://github.com/import1bones/simplex-engine).

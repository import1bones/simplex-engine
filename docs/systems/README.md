# Systems & Features

This section covers all the built-in systems and features of Simplex Engine. Each system provides specific functionality and can be customized or extended.

## 🎨 Rendering System

Graphics and visual output for your games:

### [Rendering Overview](./rendering.md)
- **Backend Support**: Debug, Pygame, OpenGL (planned)
- **Scene Graph**: Hierarchical scene organization
- **Materials & Shaders**: Visual appearance control
- **Lighting**: Directional, point, and ambient lighting

### Features
- Multiple rendering backends
- Scene graph with hierarchical transforms
- Material and shader system
- Post-processing effects
- Debug visualization

### Quick Example
```python
# Initialize renderer
renderer = Renderer(event_system=events, resource_manager=resources)
renderer.initialize({"backend": "pygame", "width": 800, "height": 600})

# Add objects to scene
ball_node = renderer.add_primitive("circle", material="ball_material")
```

## 🏃 Physics System

Physics simulation and collision detection:

### [Physics Overview](./physics.md)
- **Backend Support**: Built-in, PyBullet (planned)
- **Collision Detection**: AABB, entity-to-entity, boundary checking
- **Integration**: Direct ECS integration for entity-based physics
- **Events**: Physics collision events

### [Physics ECS Integration](./physics/physics_events_ecs_scripting.md)
- **System Integration**: Physics systems with ECS
- **Event-Driven Physics**: Physics events and scripting
- **Advanced Features**: Scripting integration for physics behavior

### Features
- Multiple physics backends
- ECS-integrated physics simulation
- Collision detection and response
- Boundary checking
- Physics events for game logic

### Quick Example
```python
# Initialize physics
physics = Physics(event_system=events, ecs=ecs_system)
physics.initialize({"backend": "builtin", "gravity": -9.81})

# Physics automatically processes entities with position and velocity components
```

## 🔊 Audio System

Sound and music playback:

### [Audio Overview](./audio.md)
- **Backend Support**: Pygame mixer
- **Sound Management**: Loading, playing, stopping sounds
- **Events**: Audio event emission
- **Resource Integration**: Works with resource manager

### Features
- Sound loading and playback
- Resource manager integration
- Audio events
- Clean resource management

### Quick Example
```python
# Initialize audio
audio = Audio(event_system=events, resource_manager=resources)

# Load and play sound
audio.load("examples/sounds/bounce.wav")
audio.play("examples/sounds/bounce.wav")
```

## 🎮 Input System

User input handling:

### [Input Overview](./input.md)
- **Backend Support**: Pygame, extensible architecture
- **Event Integration**: Input events through event system
- **Input Types**: Keyboard, mouse (gamepad planned)
- **State Management**: Input state tracking

### Features
- Multiple input backends
- Event-driven input handling
- State tracking
- Extensible input types

### Quick Example
```python
# Initialize input
input_system = Input(backend="pygame", event_system=events)

# Input events are automatically emitted and handled by input systems
```

## 📜 Scripting System

Dynamic code execution and hot-reloading:

### [Scripting Overview](./scripting.md)
- **Hot-Reloading**: Dynamic script updates during development
- **Event Hooks**: Script lifecycle events
- **Engine Access**: Scripts can access engine subsystems
- **Error Tracking**: Comprehensive error reporting

### Features
- Hot-reloading for rapid development
- Event hooks (on_load, on_reload, on_error)
- Engine subsystem access
- Error tracking and reporting
- Plugin system support

### Quick Example
```python
# Initialize script manager
scripts = ScriptManager(event_system=events, engine=engine)

# Scripts in the script directory are automatically loaded and executed
```

## 🏗️ ECS Systems

Built-in game logic systems:

### [Movement System](./ecs-systems.md#movement-system)
- Applies velocity to position components
- Boundary checking for game objects
- Configurable bounds

### [Collision System](./ecs-systems.md#collision-system)
- AABB collision detection
- Entity-to-entity collision
- Boundary collision detection
- Collision event emission

### [Input System](./ecs-systems.md#input-system)
- Processes input for entities with input components
- Player and AI input handling
- Input state management

### [Scoring System](./ecs-systems.md#scoring-system)
- Game scoring logic
- Score events
- Game state management

### Quick Example
```python
# ECS systems are automatically added during engine initialization
movement_system = MovementSystem(event_system=events, bounds=(800, 600))
ecs.add_system(movement_system)
```

## 📦 Resource Management

Asset loading and management:

### [Resource System](./resources.md)
- **Asset Types**: Shaders, textures, sounds, configurations
- **Caching**: Efficient memory usage
- **Hot-Reloading**: Dynamic asset updates
- **Analytics**: Resource usage tracking

### Features
- Multiple resource types
- Memory-efficient caching
- Hot-reloading for development
- Usage analytics
- Reference counting

## ⚙️ Configuration System

Engine and game configuration:

### [Configuration](./configuration.md)
- **TOML Format**: Human-readable configuration files
- **Hot-Reloading**: Dynamic configuration updates
- **Hierarchical**: Nested configuration structures
- **Type Safety**: Proper type handling

### Features
- TOML-based configuration
- Hot-reloading
- Hierarchical configuration
- Default value handling
- Type safety

## 🔄 Event System

Inter-system communication:

### [Event System](./events.md)
- **Event Types**: Input, physics, audio, custom events
- **Propagation**: Event bubbling and capture phases
- **Priorities**: Event handler prioritization
- **Error Handling**: Robust error handling

### Built-in Event Types
- `input` - Input events
- `physics_collision` - Collision events
- `score` - Scoring events
- `system_error` - System error reporting
- `audio_play`/`audio_stop` - Audio events

## System Integration Patterns

### Common Integration Patterns
1. **Event-Driven Communication**: Systems communicate via events
2. **Component Filtering**: Systems process only relevant entities
3. **Dependency Injection**: Systems receive required dependencies
4. **Error Isolation**: System failures don't affect other systems

### Performance Considerations
- Systems use component filtering for efficiency
- O(1) entity lookup in ECS
- Efficient event routing
- Resource caching and management

## Customization and Extension

All systems are designed to be:
- **Extensible**: Easy to add new features
- **Configurable**: Behavior can be modified via configuration
- **Replaceable**: Backend abstraction allows system replacement
- **Testable**: Clear interfaces for unit testing

## What's Next?

- Dive deeper into specific systems above
- Learn about [Advanced Topics](../advanced/) for sophisticated features
- Try [Examples & Tutorials](../examples/) to see systems in action
- Check the [API Reference](../api/) for detailed system APIs

Select a system above to learn more about its features and usage!

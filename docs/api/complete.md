# API Reference

This document provides a comprehensive API overview for the main subsystems of simplex-engine. For detailed usage examples, see the ping-pong game implementation and individual system documentation.

## Engine (`simplex.engine`)

### Core Engine Class
```python
class Engine:
    def __init__(self, config_path=None)
    
    # Properties
    .ecs                    # ECS instance
    .events                 # EventSystem instance  
    .renderer               # Renderer instance
    .config                 # Configuration management
```

### Usage Example
```python
engine = Engine(config_path="examples/ping_pong/config.toml")
engine.renderer = SimpleRenderer(width=800, height=600)
engine.renderer.set_engine_events(engine.events)
```

## ECS System (`simplex.ecs.ecs`)

### ECS Class
```python
class ECS:
    def add_entity(entity)           # Add entity to ECS
    def add_system(system)           # Register system
    def get_entity(name)            # Get entity by name
    def update()                    # Update all systems
```

### Entity Class
```python
class Entity:
    def __init__(self, name)
    def add_component(component)     # Add component to entity
    def get_component(type_name)     # Get component by type name
    def remove_component(type_name)  # Remove component
```

### System Base Class
```python
class System:
    def __init__(self, name)
    def update(entities)            # Override in subclasses
```

## Components (`simplex.ecs.components`)

### PositionComponent
```python
class PositionComponent:
    def __init__(self, x, y, z=0)
    .x, .y, .z                      # Spatial coordinates
```

### VelocityComponent
```python
class VelocityComponent:
    def __init__(self, vx, vy, vz=0)
    .vx, .vy, .vz                   # Velocity vectors
```

### CollisionComponent
```python
class CollisionComponent:
    def __init__(self, width, height, mass=1.0)
    .width, .height, .mass          # Collision properties
```

### RenderComponent
```python
class RenderComponent:
    def __init__(self, primitive='cube', color=(1, 1, 1))
    .primitive                      # 'cube', 'sphere', etc.
    .color                          # RGB color tuple (0-1 range)
```

### InputComponent
```python
class InputComponent:
    def __init__(self, input_type='player')
    .input_type                     # 'player', 'ai', etc.
    .speed                          # Movement speed
```

## Systems (`simplex.ecs.systems`)

### InputSystem
```python
class InputSystem(System):
    def __init__(self, event_system=None)
    
    # Methods
    ._handle_input_event(event)     # Process input events
    ._handle_player_input(...)      # Handle player movement
    ._handle_ai_input(...)          # Handle AI behavior
    
    # Properties
    .input_state                    # Dictionary of current key states
```

### MovementSystem
```python
class MovementSystem(System):
    def __init__(self, event_system=None, bounds=(800, 600))
    
    # Applies velocity to position
    # Handles boundary collision for entities
```

### CollisionSystem
```python
class CollisionSystem(System):
    def __init__(self, event_system=None, bounds=(800, 600))
    
    # Methods
    ._check_boundary_collision(entity)    # Check world boundaries
    ._check_entity_collision(a, b)        # Check entity-to-entity
    ._handle_collision(a, b)              # Emit collision events
```

### ScoringSystem
```python
class ScoringSystem(System):
    def __init__(self, event_system=None, bounds=(800, 600))
    
    # Properties
    .score                          # Dictionary: {'player': 0, 'ai': 0}
    
    # Methods
    ._score(scorer, ball_entity, ...)     # Handle scoring
    ._handle_score_event(event)           # Process score events
```

## Renderer (`simplex.renderer.simple_renderer`)

### SimpleRenderer Class
```python
class SimpleRenderer:
    def __init__(self, width=800, height=600)
    
    # Core Methods
    def initialize()                # Initialize pygame
    def render()                    # Render frame
    def shutdown()                  # Clean shutdown
    
    # Entity Management
    def add_entity_to_render(entity)     # Register entity for rendering
    def set_engine_events(events)        # Connect to event system
    
    # UI Methods
    def update_score(player, ai)         # Update score display
    
    # Input Handling
    def _handle_game_input(event)        # Process input events
    def _handle_debug_keys(event)        # Handle debug keys
```

## Event System (`simplex.events`)

### EventSystem Class
```python
class EventSystem:
    def register(event_type, handler, priority=0)   # Register event handler
    def emit(event_type, data)                      # Emit event
    def unregister(event_type, handler)             # Remove handler
```

### Event Types

#### Input Events
```python
event.type = 'KEYDOWN' | 'KEYUP'
event.key = 'UP' | 'DOWN'
```

#### Collision Events
```python
{
    'type': 'entity',
    'entity_a': 'entity_name',
    'entity_b': 'entity_name'
}

{
    'entity': 'entity_name',
    'type': 'boundary',
    'side': 'top' | 'bottom' | 'left' | 'right'
}
```

#### Score Events
```python
{
    'scorer': 'player' | 'ai',
    'score': {'player': int, 'ai': int}
}
```

## Usage Patterns

### Basic Game Setup
```python
from simplex.engine import Engine
from simplex.ecs.systems import InputSystem, MovementSystem, CollisionSystem
from simplex.renderer.simple_renderer import SimpleRenderer

# Initialize engine
engine = Engine()
engine.renderer = SimpleRenderer(width=800, height=600)
engine.renderer.set_engine_events(engine.events)

# Add systems
engine.ecs.add_system(InputSystem(event_system=engine.events))
engine.ecs.add_system(MovementSystem(event_system=engine.events))
engine.ecs.add_system(CollisionSystem(event_system=engine.events))
```

### Creating Game Entities
```python
from simplex.ecs.ecs import Entity
from simplex.ecs.components import *

# Create player
player = Entity('player')
player.add_component(PositionComponent(100, 300, 0))
player.add_component(VelocityComponent(0, 0, 0))
player.add_component(CollisionComponent(width=20, height=100))
player.add_component(RenderComponent(primitive='cube', color=(1, 1, 1)))

player_input = InputComponent(input_type='player')
player_input.speed = 8.0
player.add_component(player_input)

engine.ecs.add_entity(player)
engine.renderer.add_entity_to_render(player)
```

### Event Handling
```python
def handle_collision(event):
    """Custom collision handler."""
    if event.get('type') == 'entity':
        entity_a = engine.ecs.get_entity(event.get('entity_a'))
        entity_b = engine.ecs.get_entity(event.get('entity_b'))
        # Handle collision logic
        
engine.events.register('physics_collision', handle_collision)
```

### Game Loop
```python
def game_loop():
    engine.renderer.initialize()
    
    while running:
        engine.ecs.update()      # Update all systems
        engine.renderer.render() # Render frame
        # Handle win conditions, etc.
        
    engine.renderer.shutdown()
```

## Input Key Mappings

| Physical Key | Engine Event | Notes |
|-------------|--------------|-------|
| UP Arrow    | 'UP'         | Move up |
| DOWN Arrow  | 'DOWN'       | Move down |
| W Key       | 'UP'         | Alternative up |
| S Key       | 'DOWN'       | Alternative down |
| ESC         | System Exit  | Handled by renderer |
| F1-F4       | Debug        | Development tools |

## Common Patterns

### Entity Lifecycle
1. Create Entity with name
2. Add required Components
3. Register with ECS via `add_entity()`
4. Add to renderer if visual via `add_entity_to_render()`

### System Execution Order
1. InputSystem - Process input events
2. MovementSystem - Apply movement
3. CollisionSystem - Check collisions  
4. ScoringSystem - Handle game state

### Event-Driven Communication
- Systems emit events rather than calling methods directly
- Events enable loose coupling between systems
- Custom event handlers can extend game logic

## Performance Notes

- Entity component lookup is O(1) dictionary access
- System updates process all entities in single pass
- Event emission uses efficient callback mechanism
- Renderer targets 60 FPS with pygame optimization

---
For advanced usage and examples, see the ping-pong game implementation and system-specific documentation.

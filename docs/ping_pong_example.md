# Ping-Pong Game Example

## Overview

The Simplex Engine includes a complete ping-pong game that demonstrates the engine's capabilities and serves as a comprehensive example for developers. This document covers the game's implementation, features, and how to use it as a learning resource.

## Game Features

### Gameplay
- **Player vs AI**: Human player controls left paddle, AI controls right paddle
- **Responsive Controls**: W/S and UP/DOWN arrow key support with fixed input responsiveness
- **Physics Simulation**: Realistic ball bouncing with paddle collision effects
- **Spin Mechanics**: Ball spin based on hit position on paddle
- **Scoring System**: First player to reach 5 points wins
- **Real-time Updates**: Live score display and game state management

### Technical Features
- **ECS Architecture**: Complete demonstration of Entity-Component-System design
- **Event-Driven Logic**: Inter-system communication via unified event system
- **Collision Detection**: AABB collision with boundary and entity-to-entity detection
- **AI Behavior**: Intelligent paddle movement with ball tracking
- **Debug Tools**: Development overlay and logging system integration

## File Structure

```
examples/ping_pong/
├── main_gui.py        # Full-featured game with enhanced collision system
├── test_simple.py     # Simplified version for testing and debugging
└── config.toml        # Game configuration settings
```

## Running the Game

### Quick Start

```bash
# Navigate to engine directory
cd simplex-engine

# Run the simplified test version
PYTHONPATH=/path/to/simplex-engine python3 examples/ping_pong/test_simple.py

# Or run the full-featured version
PYTHONPATH=/path/to/simplex-engine python3 examples/ping_pong/main_gui.py
```

### Controls

- **W Key**: Move player paddle up
- **S Key**: Move player paddle down  
- **UP Arrow**: Move player paddle up (alternative)
- **DOWN Arrow**: Move player paddle down (alternative)
- **ESC**: Exit game
- **F1-F4**: Debug functions (when available)

## Implementation Details

### Entity Setup

#### Player Paddle
```python
player_entity = Entity('player_paddle')
player_entity.add_component(PositionComponent(50, 300, 0))     # Left side
player_entity.add_component(VelocityComponent(0, 0, 0))
player_entity.add_component(CollisionComponent(width=20, height=100, mass=0.0))
player_entity.add_component(RenderComponent(primitive='cube', color=(1, 1, 1)))

player_input = InputComponent(input_type='player')
player_input.speed = 8.0
player_entity.add_component(player_input)
```

#### AI Paddle
```python
ai_entity = Entity('ai_paddle')
ai_entity.add_component(PositionComponent(750, 300, 0))        # Right side
ai_entity.add_component(VelocityComponent(0, 0, 0))
ai_entity.add_component(CollisionComponent(width=20, height=100, mass=0.0))
ai_entity.add_component(RenderComponent(primitive='cube', color=(1, 0.5, 0.5)))

ai_input = InputComponent(input_type='ai')
ai_input.speed = 6.0  # Slightly slower than player
ai_entity.add_component(ai_input)
```

#### Ball
```python
ball_entity = Entity('ball')
ball_entity.add_component(PositionComponent(400, 300, 0))      # Center
ball_entity.add_component(VelocityComponent(6, 4, 0))          # Initial velocity
ball_entity.add_component(CollisionComponent(width=15, height=15, mass=1.0))
ball_entity.add_component(RenderComponent(primitive='sphere', color=(1, 1, 0)))
```

### System Configuration

The game uses all core ECS systems in proper order:

```python
# Create systems
input_system = InputSystem(event_system=engine.events)
movement_system = MovementSystem(event_system=engine.events, bounds=(800, 600))
collision_system = CollisionSystem(event_system=engine.events, bounds=(800, 600))
scoring_system = ScoringSystem(event_system=engine.events, bounds=(800, 600))

# Register systems in execution order
engine.ecs.add_system(input_system)      # Process input first
engine.ecs.add_system(movement_system)   # Apply movement
engine.ecs.add_system(collision_system)  # Check collisions
engine.ecs.add_system(scoring_system)    # Handle scoring
```

### Enhanced Collision Handling

The game includes sophisticated ball-paddle collision mechanics:

```python
def handle_ball_paddle_collision(event):
    """Enhanced collision between ball and paddle."""
    if event.get('type') != 'entity':
        return
    
    # Get collision entities
    entity_a = engine.ecs.get_entity(event.get('entity_a'))
    entity_b = engine.ecs.get_entity(event.get('entity_b'))
    
    # Identify ball and paddle
    if 'ball' in entity_a.name.lower():
        ball_entity, paddle_entity = entity_a, entity_b
    elif 'ball' in entity_b.name.lower():
        ball_entity, paddle_entity = entity_b, entity_a
    else:
        return
    
    # Apply collision effects
    ball_velocity = ball_entity.get_component('velocity')
    ball_pos = ball_entity.get_component('position')
    paddle_pos = paddle_entity.get_component('position')
    
    if ball_velocity and ball_pos and paddle_pos:
        # Reverse X velocity with slight speed increase
        ball_velocity.vx = -ball_velocity.vx * 1.05
        
        # Add spin based on hit position
        y_diff = ball_pos.y - paddle_pos.y
        ball_velocity.vy += y_diff * 0.1
        
        # Limit maximum velocity
        max_speed = 12
        if abs(ball_velocity.vx) > max_speed:
            ball_velocity.vx = max_speed if ball_velocity.vx > 0 else -max_speed
        if abs(ball_velocity.vy) > max_speed:
            ball_velocity.vy = max_speed if ball_velocity.vy > 0 else -max_speed

# Register collision handler
engine.events.register('physics_collision', handle_ball_paddle_collision)
```

### AI Implementation

The AI system provides intelligent opponent behavior:

```python
def _handle_ai_input(self, entity, velocity_comp, input_comp, all_entities):
    """Handle AI movement logic."""
    # Find ball entity
    ball_entity = None
    for e in all_entities:
        if 'ball' in e.name.lower():
            ball_entity = e
            break
    
    # Reset AI velocity
    velocity_comp.vy = 0
    
    if ball_entity:
        ball_pos = ball_entity.get_component('position')
        ball_vel = ball_entity.get_component('velocity')
        ai_pos = entity.get_component('position')
        
        if ball_pos and ball_vel and ai_pos:
            speed = input_comp.speed * 0.9  # AI slightly slower than player
            
            # Only track ball if it's moving towards AI
            if ball_vel.vx > 0:
                target_y = ball_pos.y
            else:
                # Return to center when ball moves away
                target_y = 300
            
            # Move towards target with deadzone to prevent jittering
            y_diff = target_y - ai_pos.y
            if abs(y_diff) > 15:  # Deadzone
                if y_diff > 0:
                    velocity_comp.vy = speed
                else:
                    velocity_comp.vy = -speed
```

### Game Loop

The main game loop handles initialization, updates, and win conditions:

```python
def simple_game_loop():
    """Simplified game loop to test core functionality."""
    print("🏓 Starting Simple Ping-Pong Test!")
    print("Controls: UP/DOWN arrows or W/S keys")
    print("Close window to quit")
    
    running = True
    frame_count = 0
    
    try:
        while running:
            frame_count += 1
            
            # Initialize renderer on first frame
            if frame_count == 1:
                engine.renderer.initialize()
            
            # Update all ECS systems
            engine.ecs.update()
            
            # Render current frame
            engine.renderer.render()
            
            # Update scores periodically
            if frame_count % 30 == 0:  # Every 30 frames (0.5 seconds at 60fps)
                player_score = scoring_system.score['player']
                ai_score = scoring_system.score['ai']
                engine.renderer.update_score(player_score, ai_score)
                
                # Check win conditions
                if player_score >= 5:
                    print(f"\n🏆 PLAYER WINS! Final Score: {player_score}-{ai_score}")
                    break
                elif ai_score >= 5:
                    print(f"\n🤖 AI WINS! Final Score: {player_score}-{ai_score}")
                    break
            
            time.sleep(0.001)  # Small delay for CPU efficiency
            
    except KeyboardInterrupt:
        print("\nGame ended by user")
    except SystemExit:
        print("\nWindow closed")
    finally:
        engine.renderer.shutdown()
```

## Learning from the Example

### ECS Design Patterns

The ping-pong game demonstrates several key ECS patterns:

1. **Component Composition**: Entities are built by combining components
2. **System Responsibilities**: Each system has a single, clear purpose
3. **Event Communication**: Systems communicate via events, not direct calls
4. **State Management**: Game state tracked through components and systems

### Event-Driven Architecture

The game shows effective event usage:

```python
# Physics events for collision handling
engine.events.register('physics_collision', handle_ball_paddle_collision)

# Score events for game state updates
engine.events.register('score', handle_score_event)

# Input events for player control
engine.events.register('input', input_system._handle_input_event)
```

### System Dependencies

The game demonstrates proper system ordering:

1. **InputSystem**: Processes player input
2. **MovementSystem**: Applies velocities to positions
3. **CollisionSystem**: Detects and handles collisions
4. **ScoringSystem**: Manages game state and win conditions

## Customization Guide

### Modifying Game Parameters

```python
# Paddle speed
player_input.speed = 10.0  # Faster player paddle
ai_input.speed = 8.0       # Faster AI paddle

# Ball physics
ball_entity.add_component(VelocityComponent(8, 6, 0))  # Faster ball

# Game bounds
MovementSystem(bounds=(1024, 768))  # Larger playing field

# Win condition
if player_score >= 10:  # Play to 10 points instead of 5
```

### Adding New Features

#### Power-ups
```python
# Create power-up entity
powerup = Entity('speed_boost')
powerup.add_component(PositionComponent(400, 200, 0))
powerup.add_component(RenderComponent(primitive='sphere', color=(0, 1, 0)))
powerup.add_component(CollisionComponent(width=20, height=20, mass=0.0))
```

#### Sound Effects
```python
# Add sound component
class SoundComponent:
    def __init__(self, sound_file):
        self.sound_file = sound_file

# Create sound system
class SoundSystem(System):
    def handle_collision_sound(self, event):
        # Play collision sound
        pass
```

#### Visual Effects
```python
# Particle system for ball trail
class ParticleComponent:
    def __init__(self):
        self.particles = []

class ParticleSystem(System):
    def update(self, entities):
        # Update particle effects
        pass
```

## Debugging and Development

### Common Issues

1. **Input Not Working**:
   - Check `engine.renderer.set_engine_events(engine.events)` is called
   - Verify InputSystem is registered
   - Enable input logging to see events

2. **Collision Detection Issues**:
   - Verify entity positions and collision bounds
   - Check CollisionSystem bounds match screen size
   - Enable collision logging

3. **AI Behavior Problems**:
   - Check ball entity name contains 'ball'
   - Verify AI speed and deadzone values
   - Add AI state logging

### Development Tools

Enable debug logging:
```python
# Add to main function
import logging
logging.basicConfig(level=logging.INFO)
```

Use debug overlay:
```python
# In SimpleRenderer
self.debug_overlay.show_fps = True
self.debug_overlay.show_entities = True
```

## Performance Optimization

### Frame Rate Management

The game targets 60 FPS with efficient update cycles:

```python
# In renderer
self.clock.tick(60)  # Limit to 60 FPS

# In game loop
time.sleep(0.001)    # Small delay to prevent CPU spinning
```

### Entity Management

- Entities are registered once during initialization
- Components are reused rather than recreated
- Systems update all entities in single passes

### Memory Efficiency

- Event objects are lightweight and short-lived
- Input state uses simple dictionary lookup
- No memory leaks from event accumulation

## Conclusion

The ping-pong game serves as an excellent introduction to the Simplex Engine's capabilities. It demonstrates proper ECS architecture, event-driven design, and provides a foundation for building more complex games. Developers can use this example to understand engine patterns and extend it with their own features and improvements.

# Input System Guide

## Overview

The Simplex Engine input system provides responsive, reliable input handling for games and interactive applications. This guide covers the architecture, usage, and recent improvements that resolved input responsiveness issues.

## Architecture

### Input Pipeline

The input system follows a unified pipeline design:

```
[Pygame Events] → [SimpleRenderer] → [Event System] → [InputSystem] → [Game Logic]
```

1. **Pygame Event Capture**: SimpleRenderer captures all pygame events in the main render loop
2. **Event Translation**: Pygame KEYDOWN/KEYUP events are translated to engine events
3. **Event Emission**: Translated events are emitted via the unified event system
4. **Input Processing**: InputSystem receives events and maintains input state
5. **Game Response**: Game systems query input state to control entity behavior

### Key Components

#### SimpleRenderer (`simplex/renderer/simple_renderer.py`)
- **Primary Event Handler**: Captures all pygame events in single location
- **Event Translation**: Converts pygame events to engine-compatible format
- **Input Forwarding**: Emits game input events via engine event system

#### InputSystem (`simplex/ecs/systems.py`)
- **Event Registration**: Registers for 'input' events during initialization
- **State Management**: Maintains dictionary of current key states
- **Player/AI Processing**: Handles different input types (player vs AI)

## Usage Examples

### Basic Input Setup

```python
from simplex.engine import Engine
from simplex.ecs.systems import InputSystem
from simplex.renderer.simple_renderer import SimpleRenderer

# Create engine and renderer
engine = Engine()
engine.renderer = SimpleRenderer(width=800, height=600)

# Connect renderer to engine event system
engine.renderer.set_engine_events(engine.events)

# Create and register input system
input_system = InputSystem(event_system=engine.events)
engine.ecs.add_system(input_system)
```

### Creating Input-Responsive Entities

```python
from simplex.ecs.ecs import Entity
from simplex.ecs.components import InputComponent, VelocityComponent

# Create player entity
player = Entity('player')
player_input = InputComponent(input_type='player')
player_input.speed = 8.0
player.add_component(player_input)
player.add_component(VelocityComponent(0, 0, 0))

engine.ecs.add_entity(player)
```

### Supported Keys

The input system currently supports:
- **UP Arrow Key**: Mapped to 'UP' event
- **DOWN Arrow Key**: Mapped to 'DOWN' event  
- **W Key**: Mapped to 'UP' event
- **S Key**: Mapped to 'DOWN' event

## Input Event Flow

### Event Structure

Input events have the following structure:
```python
event.type = 'KEYDOWN' | 'KEYUP'
event.key = 'UP' | 'DOWN'
```

### Event Processing

1. **Key Press Detection**:
   ```python
   # In SimpleRenderer._handle_game_input()
   if event.key in [pygame.K_UP, pygame.K_w]:
       game_event.type = 'KEYDOWN'
       game_event.key = 'UP'
       self.engine_events.emit('input', game_event)
   ```

2. **State Management**:
   ```python
   # In InputSystem._handle_input_event()
   if event.type == 'KEYDOWN':
       self.input_state[event.key] = True
   elif event.type == 'KEYUP':
       self.input_state[event.key] = False
   ```

3. **Movement Application**:
   ```python
   # In InputSystem._handle_player_input()
   if self.input_state.get('UP'):
       velocity_comp.vy = -speed  # Negative Y is up
   elif self.input_state.get('DOWN'):
       velocity_comp.vy = speed   # Positive Y is down
   ```

## Recent Fixes

### Problem: Single Key Press Limitation

**Issue**: Players could only press keys once - subsequent presses were ignored.

**Root Cause**: 
- Only KEYDOWN events were being processed
- Input state was set to True but never reset to False
- Keys became "stuck" in pressed state

### Solution: Complete Event Cycle Handling

**Fix 1: KEYUP Event Processing**
```python
# Added KEYUP event handling in SimpleRenderer
elif event.type == pygame.KEYUP:
    self._handle_game_input(event)
```

**Fix 2: Proper Event Type Handling**
```python
# Updated event translation to handle both event types
game_event.type = 'KEYDOWN' if event.type == pygame.KEYDOWN else 'KEYUP'
```

**Fix 3: State Cleanup**
```python
# Enhanced InputSystem to reset key state on KEYUP
elif event.type == 'KEYUP':
    self.input_state[event.key] = False
```

### Verification

The fix ensures:
- ✅ Keys can be pressed repeatedly without issues
- ✅ Proper key release detection
- ✅ Clean input state management
- ✅ Responsive controls for gameplay

## Debugging Input Issues

### Enable Input Logging

Add logging to see input events in real-time:

```python
# In SimpleRenderer._handle_game_input()
log(f"Input event emitted: {game_event.type} {game_event.key}", level="INFO")

# In InputSystem._handle_input_event()
log(f"InputSystem: Received input event - {event.type} {event.key}", level="INFO")
log(f"InputSystem: Key {event.key} state: {self.input_state}", level="INFO")
```

### Common Issues

1. **No Input Response**:
   - Check that `engine.renderer.set_engine_events(engine.events)` is called
   - Verify InputSystem is registered with ECS
   - Ensure entity has InputComponent

2. **Sticky Input**:
   - Verify KEYUP events are being processed
   - Check input state is being reset to False on key release

3. **Multiple Event Handlers**:
   - Ensure only one pygame.event.get() call per frame
   - Use unified input pipeline through SimpleRenderer

## Performance Considerations

### Event Processing Efficiency

- Input events are processed once per frame in the render loop
- State lookup is O(1) dictionary access
- Event emission uses efficient callback system

### Memory Management

- Input state dictionary only stores active keys
- Event objects are lightweight and garbage collected automatically
- No memory leaks from event accumulation

## Future Enhancements

### Planned Features
- **Gamepad Support**: Xbox/PlayStation controller input
- **Touch Input**: Mobile and tablet touch handling  
- **Key Binding**: Customizable key mappings
- **Input Buffering**: Frame-perfect input for competitive games
- **Mouse Support**: Mouse movement and click events

### Extensibility

The input system is designed for easy extension:

```python
# Adding new input types
class CustomInputComponent(InputComponent):
    def __init__(self, input_type='custom'):
        super().__init__(input_type)
        self.custom_bindings = {}

# Adding new key mappings
def _handle_game_input(self, event):
    # Add new key mappings here
    if event.key == pygame.K_SPACE:
        game_event.key = 'SPACE'
        self.engine_events.emit('input', game_event)
```

## Best Practices

### Input System Setup
1. Always connect renderer to engine events before game loop
2. Register InputSystem before other systems that depend on input
3. Create InputComponent with appropriate speed values
4. Use consistent input_type naming ('player', 'ai', etc.)

### Game Design
1. Provide visual feedback for input responsiveness
2. Handle edge cases like simultaneous key presses
3. Test input on different hardware and frame rates
4. Consider accessibility requirements for input alternatives

### Debugging
1. Enable input logging during development
2. Test all supported key combinations
3. Verify input state cleanup on game state changes
4. Monitor for input lag or responsiveness issues

## Conclusion

The Simplex Engine input system provides a robust, extensible foundation for game input handling. With the recent fixes addressing key responsiveness issues, developers can now create responsive, engaging gameplay experiences with confidence in the input system's reliability.

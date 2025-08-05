# Advanced Example Project: Custom Platformer

This example demonstrates how to build a simple platformer game using simplex-engine, integrating ECS, Renderer, Physics, Input, and scripting.

## Features
- Player movement and jumping
- Platform collision
- Custom event handling
- Scripted win condition

## Example Code
```python
from simplex.engine import Engine
from simplex.physics.body import RigidBody
from simplex.event.event_system import EventSystem

engine = Engine()

# Player entity with physics
player = RigidBody('Player', mass=1.0)
engine.physics.add_rigid_body(player)

# Platform entity (static)
platform = RigidBody('Platform', mass=0.0)
engine.physics.add_rigid_body(platform)

# Add player and platform to renderer
engine.renderer.add_primitive('cube', material='player_mat')
engine.renderer.add_primitive('cube', material='platform_mat')

# Input event: jump
engine.input.on_event('jump', lambda e: player.apply_impulse((0, 10, 0)))

# Win condition: player reaches height
engine.events.register('physics_update', lambda e: print('You win!') if player.position[1] > 10 else None)

engine.run()
```

## Extending This Example
- Add more platforms and obstacles
- Implement scoring and UI
- Use ScriptManager for more complex logic

---
For more, see subsystem docs and the full integration demo.

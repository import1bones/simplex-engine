# Advanced Example: Full Engine Integration

This example demonstrates how to integrate all major subsystems: ECS, Renderer, Physics, Input, and Scripting.

## Example Code
```python
from simplex.engine import Engine
from simplex.event.event_system import EventSystem
from simplex.physics.body import RigidBody

engine = Engine()

# Register a custom event handler
engine.events.register('physics_collision', lambda e: print('Collision:', e))

# Add a rigid body to the physics system
ball = RigidBody('Ball')
engine.physics.add_rigid_body(ball)

# Add a primitive to the renderer
engine.renderer.add_primitive('cube', material=None)

# Run the engine (single tick for demo)
engine.run()
```

## Notes
- See subsystem docs for more advanced usage.
- Extend this example to add scripting, resource hot-reloading, and more.

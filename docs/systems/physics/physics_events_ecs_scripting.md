# Exposing Physics Events to ECS and Scripting (MVP-3)

The Physics subsystem emits events (e.g., collisions) via the EventSystem. ECS systems and scripts can subscribe to these events for custom logic.

## Usage Example
```python
from simplex.physics.physics import Physics
from simplex.event.event_system import EventSystem

events = EventSystem()
physics = Physics(event_system=events)

def on_collision(event):
    print(f"Collision event: {event['a']} <-> {event['b']}")

events.register('physics_collision', on_collision)

# Add bodies and simulate
from simplex.physics.body import RigidBody
body1 = RigidBody('A')
body2 = RigidBody('B')
physics.add_rigid_body(body1)
physics.add_rigid_body(body2)
physics.simulate()
```

## Scripting Integration
- Scripts can register event handlers using the same EventSystem interface.
- Example:
```python
def on_collision(event):
    # Custom script logic
    pass
engine.events.register('physics_collision', on_collision)
```

## Notes
- All physics events are observable and extensible.
- See `simplex/physics/physics.py` for event emission details.

# Advanced Physics Features (MVP-3)

The Physics subsystem supports:
- Rigid body simulation (see `RigidBody`)
- Soft body simulation (see `SoftBody`)
- Collision detection and response (stubbed, extensible)
- Event emission for collisions (see `physics_collision` event)

## Usage Example
```python
from simplex.physics.physics import Physics
from simplex.physics.body import RigidBody, SoftBody
from simplex.event.event_system import EventSystem

events = EventSystem()
physics = Physics(event_system=events)

ball = RigidBody('Ball', mass=1.0)
wall = RigidBody('Wall', mass=0.0)
cloth = SoftBody('Cloth', points=[(0,0,0), (1,0,0), (0,1,0)])
physics.add_rigid_body(ball)
physics.add_rigid_body(wall)
physics.add_soft_body(cloth)

physics.simulate()
```

## Extending
- Implement real simulation and collision response in `simulate` and `step_collision_response`.
- Add more body types or constraints as needed.

See also: `examples/physics_demo.py`, `docs/physics_demo_scene.md`.

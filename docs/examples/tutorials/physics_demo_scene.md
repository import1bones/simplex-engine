# Physics-Based Demo Scene (MVP-3)

This demo shows how to use the Physics subsystem, handle collision events, and integrate with ECS/scripting.

## How to Run
```bash
python examples/physics_demo.py
```

## What It Does
- Creates two rigid bodies (a ball and a wall)
- Registers a collision event handler
- Runs a physics simulation step (collision detection is stubbed)
- Prints collision events to the console

## Example Output
```
[DEMO] Simulating physics...
[DEMO] Collision event: <RigidBody Ball pos=(0, 0, 0) vel=(1, 0, 0)> <-> <RigidBody Wall pos=(5, 0, 0) vel=(0, 0, 0)>
```

## Extending
- Add more bodies, soft bodies, or custom collision logic
- Integrate with ECS to update entity components on collision
- Use scripting to define custom event handlers

## See Also
- `simplex/physics/physics.py`
- `simplex/physics/body.py`
- `docs/physics_events_ecs_scripting.md`

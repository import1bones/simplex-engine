"""Shared ECS setup for ping-pong examples."""

from simplex.ecs.systems import (
    CollisionSystem,
    InputSystem,
    MovementSystem,
    ScoringSystem,
)

_DROP_SYSTEMS = {
    "movement",
    "collision",
    "input",
    "scoring",
    "player_control",
    "voxel_collision",
    "chunk_streaming",
    "chunk",
    "chunk_mesh",
}


def install_ping_pong_systems(engine, bounds=(800, 600)):
    """Replace default engine systems with a single ping-pong ECS stack."""
    engine.ecs.systems = [s for s in engine.ecs.systems if s.name not in _DROP_SYSTEMS]

    input_system = InputSystem(event_system=engine.events, bounds=bounds)
    movement_system = MovementSystem(event_system=engine.events, bounds=bounds)
    collision_system = CollisionSystem(event_system=engine.events, bounds=bounds)
    scoring_system = ScoringSystem(event_system=engine.events, bounds=bounds)

    for system in (input_system, movement_system, collision_system, scoring_system):
        engine.ecs.add_system(system)

    return input_system, movement_system, collision_system, scoring_system

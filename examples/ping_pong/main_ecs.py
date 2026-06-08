"""
main_ecs.py - Ping-Pong Game with Proper ECS Architecture (MVP-5 Priority 1 Fix)

A refactored ping-pong game that properly uses simplex-engine's ECS subsystem
for entity management, with proper component composition and system architecture.
"""

from simplex.engine import Engine
from simplex.ecs.components import (
    PositionComponent,
    VelocityComponent,
    RenderComponent,
    CollisionComponent,
    InputComponent,
    ScoreComponent,
)
from simplex.ecs.systems import (
    MovementSystem,
    CollisionSystem,
    InputSystem,
    ScoringSystem,
)
from simplex.ecs.ecs import Entity
from simplex.renderer.material import Material

# --- Game Setup ---
engine = Engine(config_path="examples/ping_pong/config.toml")

# Create ECS systems and register them
input_system = InputSystem(event_system=engine.events)
movement_system = MovementSystem(event_system=engine.events)
collision_system = CollisionSystem(event_system=engine.events, bounds=(800, 600))
scoring_system = ScoringSystem(event_system=engine.events, bounds=(800, 600))

engine.ecs.add_system(input_system)
engine.ecs.add_system(movement_system)
engine.ecs.add_system(collision_system)
engine.ecs.add_system(scoring_system)

# Create game entities with proper ECS composition
# Player paddle entity
player_entity = Entity("player_paddle")
player_entity.add_component(PositionComponent(50, 300, 0))
player_entity.add_component(VelocityComponent(0, 0, 0))
player_entity.add_component(CollisionComponent(width=20, height=100, mass=0.0))
player_entity.add_component(RenderComponent(primitive="cube", color=(1, 1, 1)))
player_entity.add_component(InputComponent(input_type="player"))
engine.ecs.add_entity(player_entity)

# AI paddle entity
ai_entity = Entity("ai_paddle")
ai_entity.add_component(PositionComponent(750, 300, 0))
ai_entity.add_component(VelocityComponent(0, 0, 0))
ai_entity.add_component(CollisionComponent(width=20, height=100, mass=0.0))
ai_entity.add_component(RenderComponent(primitive="cube", color=(0, 1, 0)))
ai_entity.add_component(InputComponent(input_type="ai"))
engine.ecs.add_entity(ai_entity)

# Ball entity
ball_entity = Entity("ball")
ball_entity.add_component(PositionComponent(400, 300, 0))
ball_entity.add_component(VelocityComponent(-6, 4, 0))
ball_entity.add_component(CollisionComponent(width=15, height=15, mass=1.0))
ball_entity.add_component(RenderComponent(primitive="sphere", color=(1, 0, 0)))
engine.ecs.add_entity(ball_entity)

# Register materials for rendering
player_mat = Material("player_mat", properties={"color": (1, 1, 1)})
ai_mat = Material("ai_mat", properties={"color": (0, 1, 0)})
ball_mat = Material("ball_mat", properties={"color": (1, 0, 0)})
engine.renderer.register_material(player_mat)
engine.renderer.register_material(ai_mat)
engine.renderer.register_material(ball_mat)

# Add primitives to renderer (this will be enhanced with actual rendering later)
engine.renderer.add_primitive("cube", material="player_mat")
engine.renderer.add_primitive("cube", material="ai_mat")
engine.renderer.add_primitive("sphere", material="ball_mat")


# Event handlers for game events
def on_collision(event):
    """Handle collision events."""
    if isinstance(event, dict):
        if event.get("type") == "boundary":
            print(f"[Collision] {event['entity']} hit {event['side']} boundary")
        elif event.get("type") == "entity":
            print(f"[Collision] {event['entity_a']} collided with {event['entity_b']}")


def on_input(event):
    """Handle input events for CLI mode."""
    # Input system will handle this automatically
    pass


# Register event handlers
engine.events.register("physics_collision", on_collision)
engine.events.register("input", on_input)


# Game loop
def game_loop():
    """Main game loop with proper ECS update."""
    import time

    print("Starting ECS-based Ping-Pong Game...")
    print("Controls: UP/DOWN arrows or W/S keys")
    print("Press Ctrl+C to quit")

    try:
        while True:
            # Poll input
            engine.input.poll()

            # Update ECS systems (this is where the magic happens)
            engine.ecs.update()

            # Render (currently just logs)
            engine.renderer.render()

            # Simple CLI display of positions
            player_pos = player_entity.get_component("position")
            ai_pos = ai_entity.get_component("position")
            ball_pos = ball_entity.get_component("position")

            print(
                f"\r[CLI] Player Y:{player_pos.y:3.0f} | Ball: ({ball_pos.x:3.0f},{ball_pos.y:3.0f}) | AI Y:{ai_pos.y:3.0f} | Score: P:{scoring_system.score['player']} AI:{scoring_system.score['ai']}",
                end="",
            )

            time.sleep(0.05)  # ~20 FPS

    except KeyboardInterrupt:
        print("\nGame ended by user")


if __name__ == "__main__":
    game_loop()

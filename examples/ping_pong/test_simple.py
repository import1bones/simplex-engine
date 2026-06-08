"""
Simple test version of ping-pong game to debug core issues.
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
from simplex.renderer.simple_renderer import SimpleRenderer
import time

# --- Simple Game Setup ---
engine = Engine(config_path="examples/ping_pong/config.toml")

# Replace stub renderer with actual GUI renderer
engine.renderer = SimpleRenderer(width=800, height=600)
# Connect renderer to engine event system for input forwarding
engine.renderer.set_engine_events(engine.events)

# Create ECS systems in correct order
movement_system = MovementSystem(event_system=engine.events, bounds=(800, 600))
input_system = InputSystem(event_system=engine.events)
collision_system = CollisionSystem(event_system=engine.events, bounds=(800, 600))
scoring_system = ScoringSystem(event_system=engine.events, bounds=(800, 600))

# Add systems in the correct order
engine.ecs.add_system(input_system)
engine.ecs.add_system(movement_system)
engine.ecs.add_system(collision_system)
engine.ecs.add_system(scoring_system)

# Create game entities
# Player paddle
player_entity = Entity("player_paddle")
player_entity.add_component(PositionComponent(50, 300, 0))
player_entity.add_component(VelocityComponent(0, 0, 0))
player_entity.add_component(CollisionComponent(width=20, height=100, mass=0.0))
player_entity.add_component(RenderComponent(primitive="cube", color=(1, 1, 1)))
player_input = InputComponent(input_type="player")
player_input.speed = 8.0
player_entity.add_component(player_input)
engine.ecs.add_entity(player_entity)
engine.renderer.add_entity_to_render(player_entity)

# AI paddle
ai_entity = Entity("ai_paddle")
ai_entity.add_component(PositionComponent(750, 300, 0))
ai_entity.add_component(VelocityComponent(0, 0, 0))
ai_entity.add_component(CollisionComponent(width=20, height=100, mass=0.0))
ai_entity.add_component(RenderComponent(primitive="cube", color=(1, 0.5, 0.5)))
ai_input = InputComponent(input_type="ai")
ai_input.speed = 6.0
ai_entity.add_component(ai_input)
engine.ecs.add_entity(ai_entity)
engine.renderer.add_entity_to_render(ai_entity)

# Ball entity
ball_entity = Entity("ball")
ball_entity.add_component(PositionComponent(400, 300, 0))
ball_entity.add_component(VelocityComponent(6, 4, 0))
ball_entity.add_component(CollisionComponent(width=15, height=15, mass=1.0))
ball_entity.add_component(RenderComponent(primitive="sphere", color=(1, 1, 0)))
engine.ecs.add_entity(ball_entity)
engine.renderer.add_entity_to_render(ball_entity)


# Enhanced collision handling for ping-pong
def handle_ball_paddle_collision(event):
    """Enhanced collision between ball and paddle."""
    if event.get("type") != "entity":
        return

    entity_a_name = event.get("entity_a")
    entity_b_name = event.get("entity_b")

    if not entity_a_name or not entity_b_name:
        return

    entity_a = engine.ecs.get_entity(entity_a_name)
    entity_b = engine.ecs.get_entity(entity_b_name)

    if not entity_a or not entity_b:
        return

    if "ball" in entity_a.name.lower():
        ball_entity, paddle_entity = entity_a, entity_b
    elif "ball" in entity_b.name.lower():
        ball_entity, paddle_entity = entity_b, entity_a
    else:
        return

    ball_velocity = ball_entity.get_component("velocity")
    ball_pos = ball_entity.get_component("position")
    paddle_pos = paddle_entity.get_component("position")

    if ball_velocity and ball_pos and paddle_pos:
        # Reverse X velocity and add Y spin based on where ball hits paddle
        ball_velocity.vx = -ball_velocity.vx * 1.05  # Slight speed increase

        # Add spin based on hit position
        y_diff = ball_pos.y - paddle_pos.y
        ball_velocity.vy += y_diff * 0.1

        # Limit max velocity
        max_speed = 12
        if abs(ball_velocity.vx) > max_speed:
            ball_velocity.vx = max_speed if ball_velocity.vx > 0 else -max_speed
        if abs(ball_velocity.vy) > max_speed:
            ball_velocity.vy = max_speed if ball_velocity.vy > 0 else -max_speed


# Register enhanced collision handler
engine.events.register("physics_collision", handle_ball_paddle_collision)


# Simple game loop
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

            # Initialize renderer
            if frame_count == 1:
                engine.renderer.initialize()

            # Update ECS systems
            engine.ecs.update()

            # Render frame
            engine.renderer.render()

            # Update scores in renderer
            if frame_count % 30 == 0:  # Update every half second
                player_score = scoring_system.score["player"]
                ai_score = scoring_system.score["ai"]
                engine.renderer.update_score(player_score, ai_score)

                # Check win condition
                if player_score >= 5:
                    print(f"\n🏆 PLAYER WINS! Final Score: {player_score}-{ai_score}")
                    break
                elif ai_score >= 5:
                    print(f"\n🤖 AI WINS! Final Score: {player_score}-{ai_score}")
                    break

            time.sleep(0.001)

    except KeyboardInterrupt:
        print("\nGame ended by user")
    except SystemExit:
        print("\nWindow closed")
    finally:
        engine.renderer.shutdown()


if __name__ == "__main__":
    simple_game_loop()

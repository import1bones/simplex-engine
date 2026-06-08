"""
main_gui.py - Ping-Pong Game with Full ECS + GUI Rendering (MVP-5 Priority 1&2 Complete)

A fully integrated ping-pong game that uses:
1. Proper ECS architecture with components and systems
2. Actual GUI rendering with pygame
3. Event-driven design throughout
4. Physics subsystem integration
"""

import os
import sys

_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, _root)
sys.path.insert(0, os.path.dirname(__file__))

from simplex.engine import Engine
from simplex.ecs.components import (
    PositionComponent,
    VelocityComponent,
    RenderComponent,
    CollisionComponent,
    InputComponent,
    ScoreComponent,
)
from simplex.ecs.ecs import Entity
from simplex.ecs.systems import CollisionSystem
from simplex.renderer.simple_renderer import SimpleRenderer
from ecs_setup import install_ping_pong_systems
import time

# --- Game Setup ---
engine = Engine(config_path="examples/ping_pong/config.toml")

# Replace stub renderer with actual GUI renderer
engine.renderer = SimpleRenderer(width=800, height=600)
# Connect renderer to engine event system for input forwarding
engine.renderer.set_engine_events(engine.events)

_, _, _, scoring_system = install_ping_pong_systems(engine, bounds=(800, 600))

# Create game entities with proper ECS composition
# Player paddle entity
player_entity = Entity("player_paddle")
player_entity.add_component(PositionComponent(50, 300, 0))
player_entity.add_component(VelocityComponent(0, 0, 0))
player_entity.add_component(CollisionComponent(width=20, height=100, mass=0.0))
player_entity.add_component(RenderComponent(primitive="cube", color=(1, 1, 1)))
player_entity.add_component(InputComponent(input_type="player"))
engine.ecs.add_entity(player_entity)
engine.renderer.add_entity_to_render(player_entity)

# AI paddle entity
ai_entity = Entity("ai_paddle")
ai_entity.add_component(PositionComponent(750, 300, 0))
ai_entity.add_component(VelocityComponent(0, 0, 0))
ai_entity.add_component(CollisionComponent(width=20, height=100, mass=0.0))
ai_entity.add_component(RenderComponent(primitive="cube", color=(0, 1, 0)))
ai_entity.add_component(InputComponent(input_type="ai"))
engine.ecs.add_entity(ai_entity)
engine.renderer.add_entity_to_render(ai_entity)

# Ball entity
ball_entity = Entity("ball")
ball_entity.add_component(PositionComponent(400, 300, 0))
ball_entity.add_component(VelocityComponent(-3, 2, 0))  # Slower for better gameplay
ball_entity.add_component(CollisionComponent(width=15, height=15, mass=1.0))
ball_entity.add_component(RenderComponent(primitive="sphere", color=(1, 0, 0)))
engine.ecs.add_entity(ball_entity)
engine.renderer.add_entity_to_render(ball_entity)


# Enhanced collision system for paddle-ball interactions
class PaddleBallCollisionSystem(CollisionSystem):
    """Enhanced collision system that handles paddle-ball physics."""

    def _handle_collision(self, entity_a, entity_b):
        """Enhanced collision handling for paddle-ball interactions."""
        super()._handle_collision(entity_a, entity_b)

        # Determine which is ball and which is paddle
        ball_entity = None
        paddle_entity = None

        if "ball" in entity_a.name.lower():
            ball_entity, paddle_entity = entity_a, entity_b
        elif "ball" in entity_b.name.lower():
            ball_entity, paddle_entity = entity_b, entity_a
        else:
            return  # Not a ball-paddle collision

        # Handle ball-paddle collision physics
        ball_velocity = ball_entity.get_component("velocity")
        if ball_velocity:
            # Reverse X velocity and add some randomness
            ball_velocity.vx = -ball_velocity.vx
            # Add slight Y velocity variation based on where ball hits paddle
            ball_pos = ball_entity.get_component("position")
            paddle_pos = paddle_entity.get_component("position")
            if ball_pos and paddle_pos:
                y_diff = ball_pos.y - paddle_pos.y
                ball_velocity.vy += y_diff * 0.1  # Add spin effect


# Replace collision system with enhanced version
engine.ecs.systems = [s for s in engine.ecs.systems if s.name != "collision"]
enhanced_collision = PaddleBallCollisionSystem(
    event_system=engine.events, bounds=(800, 600)
)
engine.ecs.add_system(enhanced_collision)


# Event handlers for game feedback
def on_collision(event):
    """Handle collision events with sound/feedback."""
    if isinstance(event, dict):
        if event.get("type") == "boundary":
            print(f"[Audio] Ball boundary hit sound")
        elif event.get("type") == "entity":
            print(f"[Audio] Paddle hit sound")


def on_score(event):
    """Handle score events."""
    if isinstance(event, dict) and "scorer" in event:
        scorer = event["scorer"]
        score = event.get("score", {})
        print(f"\n🎉 {scorer.title()} SCORES! 🎉")
        print(f"Score: Player {score.get('player', 0)} - {score.get('ai', 0)} AI")

        # Update renderer score display
        engine.renderer.update_score(score.get("player", 0), score.get("ai", 0))


# Register event handlers
engine.events.register("physics_collision", on_collision)
engine.events.register("score", on_score)


# Game loop
def game_loop():
    """Main GUI game loop with full ECS integration and debug features."""
    print("🏓 Starting Simplex Engine Ping-Pong!")
    print("Controls: UP/DOWN arrows or W/S keys")
    print("Debug Controls: F1=Debug, F2=Pause, F3=Step, ESC=Quit")
    print("First to 5 points wins!")
    print("Close window to quit")

    running = True
    frame_count = 0

    try:
        while running:
            frame_count += 1

            # Initialize renderer on first frame
            if frame_count == 1:
                engine.renderer.initialize()

            # Check if systems should update (respects pause state)
            if engine.renderer.should_update_systems():
                # Update ECS systems (core game logic)
                engine.ecs.update()

                # Integrate physics with ECS
                if hasattr(engine.physics, "simulate_ecs"):
                    # Use ECS-integrated physics (already handled by ECS systems)
                    pass

                # Check win condition (only when not paused)
                if frame_count % 60 == 0:  # Check every second
                    player_score = scoring_system.score["player"]
                    ai_score = scoring_system.score["ai"]

                    # Update renderer with current scores
                    engine.renderer.update_score(player_score, ai_score)

                    if player_score >= 5:
                        print(
                            f"\n🏆 PLAYER WINS! Final Score: {player_score}-{ai_score}"
                        )
                        break
                    elif ai_score >= 5:
                        print(f"\n🤖 AI WINS! Final Score: {player_score}-{ai_score}")
                        break

            # Always render frame (shows pause overlay when paused)
            engine.renderer.render()

            # Frame rate control (handled by renderer)
            time.sleep(0.001)

    except KeyboardInterrupt:
        print("\nGame ended by user")
    except SystemExit:
        print("\nWindow closed")
    finally:
        engine.renderer.shutdown()


if __name__ == "__main__":
    game_loop()

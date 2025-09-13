"""
Full engine integration demo for simplex-engine MVP-3.
Demonstrates ECS, Renderer, Physics, Input, and Scripting integration.
"""

from simplex.engine import Engine
from simplex.event.event_system import EventSystem
from simplex.physics.body import RigidBody


def run_full_integration_demo():
    engine = Engine()
    engine.events.register("physics_collision", lambda e: print("Collision:", e))
    ball = RigidBody("Ball")
    engine.physics.add_rigid_body(ball)
    engine.renderer.add_primitive("cube", material=None)
    engine.run()


if __name__ == "__main__":
    run_full_integration_demo()

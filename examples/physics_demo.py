"""
Physics-based demo scene for simplex-engine MVP-3.
Demonstrates rigid body creation, collision events, and ECS integration.
"""

from simplex.physics.physics import Physics
from simplex.physics.body import RigidBody
from simplex.event.event_system import EventSystem


def run_physics_demo():
    events = EventSystem()
    physics = Physics(event_system=events)

    def on_collision(event):
        print(f"[DEMO] Collision event: {event['a']} <-> {event['b']}")

    events.register("physics_collision", on_collision)

    # Create demo rigid bodies
    ball = RigidBody("Ball", mass=1.0, position=(0, 0, 0), velocity=(1, 0, 0))
    wall = RigidBody("Wall", mass=0.0, position=(5, 0, 0), velocity=(0, 0, 0))
    physics.add_rigid_body(ball)
    physics.add_rigid_body(wall)

    # Simulate (collision detection is stubbed)
    print("[DEMO] Simulating physics...")
    physics.simulate()


if __name__ == "__main__":
    run_physics_demo()

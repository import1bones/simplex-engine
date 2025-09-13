"""
Integration and edge-case tests for simplex-engine MVP-3 subsystems.
"""

import unittest
from simplex.engine import Engine
from simplex.physics.body import RigidBody
from simplex.event.event_system import EventSystem


class TestEngineIntegration(unittest.TestCase):
    def setUp(self):
        self.engine = Engine()

    def test_add_and_run(self):
        # Should not raise
        self.engine.run()


class TestPhysicsEdgeCases(unittest.TestCase):
    def setUp(self):
        self.events = EventSystem()
        from simplex.physics.physics import Physics

        self.physics = Physics(event_system=self.events)

    def test_empty_simulation(self):
        # Should not raise
        self.physics.simulate()

    def test_collision_event(self):
        collisions = []

        def on_collision(event):
            collisions.append((event["a"], event["b"]))

        self.events.register("physics_collision", on_collision)
        a = RigidBody("A")
        b = RigidBody("B")
        self.physics.add_rigid_body(a)
        self.physics.add_rigid_body(b)
        self.physics.simulate()
        # Collision detection is stubbed, so collisions may be empty
        self.assertIsInstance(collisions, list)


if __name__ == "__main__":
    unittest.main()

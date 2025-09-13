"""
Integration and edge-case tests for simplex-engine MVP-3 subsystems.
"""

import unittest
from simplex.engine import Engine
from simplex.physics.body import RigidBody, SoftBody
from simplex.event.event_system import EventSystem
from simplex.resource.resource_manager import ResourceManager
from simplex.input.input import Input


class TestEngineIntegration(unittest.TestCase):
    def setUp(self):
        self.engine = Engine()

    def test_run(self):
        # Should not raise
        self.engine.run()


class TestPhysicsEdgeCases(unittest.TestCase):
    def setUp(self):
        self.events = EventSystem()
        from simplex.physics.physics import Physics

        self.physics = Physics(event_system=self.events)

    def test_empty_simulation(self):
        self.physics.simulate()

    def test_rigid_and_soft_body(self):
        a = RigidBody("A")
        b = SoftBody("B")
        self.physics.add_rigid_body(a)
        self.physics.add_soft_body(b)
        self.physics.simulate()


class TestResourceManagerEdgeCases(unittest.TestCase):
    def setUp(self):
        self.rm = ResourceManager()

    def test_load_unload_nonexistent(self):
        self.rm.load("nonexistent.file")
        self.rm.unload("nonexistent.file")
        analytics = self.rm.get_usage_analytics()
        self.assertIn("recent_errors", analytics)


class TestInputEdgeCases(unittest.TestCase):
    def setUp(self):
        self.input = Input(backend="custom")

    def test_poll_custom_backend(self):
        self.input.poll()

    def test_get_state_custom_backend(self):
        state = self.input.get_state()
        self.assertIn("custom", state)


if __name__ == "__main__":
    unittest.main()

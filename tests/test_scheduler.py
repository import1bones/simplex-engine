import unittest
from simplex.scheduler.manager import SubsystemManager


class EngineStub:
    pass


class TestSubsystemManager(unittest.TestCase):
    def test_register_and_ensure_creates_attribute(self):
        eng = EngineStub()
        sched = SubsystemManager(eng)

        def make_events(e):
            return {'name': 'events'}

        sched.register_factory('events', make_events, requires=[])
        self.assertNotIn('events', sched.created())

        inst = sched.ensure('events')
        self.assertIsNotNone(inst)
        self.assertTrue(hasattr(eng, 'events'))
        self.assertIn('events', sched.created())
        self.assertEqual(getattr(eng, 'events'), inst)

    def test_dependency_resolution_order(self):
        eng = EngineStub()
        sched = SubsystemManager(eng)

        def make_a(e):
            return 'A'

        def make_b(e):
            # b expects a to exist on engine
            return f"B(dep={getattr(e, 'a', None)})"

        sched.register_factory('a', make_a, requires=[])
        sched.register_factory('b', make_b, requires=['a'])

        sched.ensure('b')
        self.assertIn('a', sched.created())
        self.assertIn('b', sched.created())
        self.assertEqual(getattr(eng, 'a'), 'A')
        self.assertEqual(getattr(eng, 'b'), 'B(dep=A)')

    def test_initialize_all_creates_every_registered(self):
        eng = EngineStub()
        sched = SubsystemManager(eng)

        sched.register_factory('x', lambda e: 1, requires=[])
        sched.register_factory('y', lambda e: 2, requires=['x'])

        sched.initialize_all()
        self.assertTrue(hasattr(eng, 'x'))
        self.assertTrue(hasattr(eng, 'y'))
        self.assertIn('x', sched.created())
        self.assertIn('y', sched.created())

    def test_missing_factory_raises(self):
        eng = EngineStub()
        sched = SubsystemManager(eng)
        with self.assertRaises(KeyError):
            sched.ensure('unknown')

    def test_self_dependency_raises(self):
        eng = EngineStub()
        sched = SubsystemManager(eng)
        sched.register_factory('loop', lambda e: None, requires=['loop'])
        with self.assertRaises(RuntimeError):
            sched.ensure('loop')


if __name__ == '__main__':
    unittest.main()

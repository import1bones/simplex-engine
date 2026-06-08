import unittest

from simplex.ecs.chunk_streaming_system import ChunkStreamingSystem
from simplex.ecs.components import PositionComponent
from simplex.ecs.ecs import ECS, Entity
from simplex.world.chunk_manager import ChunkManager


class ChunkStreamingTests(unittest.TestCase):
    def setUp(self):
        self.ecs = ECS()
        self.cm = ChunkManager(self.ecs, chunk_size=(16, 16, 16), cache_size=32)

        class _Engine:
            pass

        self.engine = _Engine()
        self.engine.ecs = self.ecs
        self.engine.chunk_manager = self.cm

        self.system = ChunkStreamingSystem(
            engine=self.engine,
            radius=1,
            horizontal_only=True,
            stream_y_chunk=0,
            hysteresis=4.0,
        )
        self.ecs.add_system(self.system)

        self.player = Entity("Player")
        self.player.add_component(PositionComponent(0.5, 8.0, 0.5))
        self.ecs.add_entity(self.player)

    def test_vertical_motion_does_not_change_stream_center(self):
        pos = self.player.get_component("position")
        self.ecs.update()
        first = self.system._last_center
        self.assertEqual(first[1], 0)

        pos.y = 20.0
        self.ecs.update()
        self.assertEqual(self.system._last_center, first)

        pos.y = 2.0
        self.ecs.update()
        self.assertEqual(self.system._last_center, first)

    def test_hysteresis_avoids_border_flutter(self):
        pos = self.player.get_component("position")
        self.ecs.update()
        self.assertEqual(self.system._last_center[0], 0)

        pos.x = 17.0
        self.ecs.update()
        self.assertEqual(self.system._last_center[0], 0)

        pos.x = 20.0
        self.ecs.update()
        self.assertEqual(self.system._last_center[0], 1)


if __name__ == "__main__":
    unittest.main()

import unittest

from simplex.ecs.ecs import ECS, Entity
from simplex.ecs.components import PositionComponent
from simplex.ecs.voxel_collision_system import VoxelCollisionSystem
from simplex.world.chunk_manager import ChunkManager
from simplex.voxel.voxel import BLOCK_DIRT


class VoxelCollisionTests(unittest.TestCase):
    def setUp(self):
        self.ecs = ECS()
        self.cm = ChunkManager(self.ecs, chunk_size=(16, 16, 16), cache_size=8)
        self.cm.create_chunk((0, 0, 0))
        chunk = self.cm.get_chunk((0, 0, 0))
        for y in range(4):
            chunk.set_block_id(0, y, 0, BLOCK_DIRT)

        class _Engine:
            pass

        self.engine = _Engine()
        self.engine.ecs = self.ecs
        self.engine.chunk_manager = self.cm
        self.engine._last_delta_time = 1.0 / 60.0

        self.system = VoxelCollisionSystem(engine=self.engine)
        self.player = Entity("Player")
        self.player.add_component(PositionComponent(0.5, 10.0, 0.5))
        self.ecs.add_entity(self.player)

    def test_gravity_snaps_player_to_ground(self):
        for _ in range(120):
            self.system.update(self.ecs.entities)
        pos = self.player.get_component("position")
        self.assertAlmostEqual(pos.y, 4.0, delta=0.2)
        self.assertTrue(self.system._on_ground.get("Player", False))


if __name__ == "__main__":
    unittest.main()

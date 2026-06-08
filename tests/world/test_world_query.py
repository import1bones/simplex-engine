import unittest

from simplex.ecs.ecs import ECS
from simplex.world.chunk_manager import ChunkManager
from simplex.world.world_query import (
    find_ground_height,
    get_block_id_at_world,
    is_solid_at_world,
    world_to_chunk_coords,
    world_to_local,
)
from simplex.voxel.voxel import BLOCK_AIR, BLOCK_DIRT


class WorldQueryTests(unittest.TestCase):
    def setUp(self):
        self.ecs = ECS()
        self.cm = ChunkManager(self.ecs, chunk_size=(16, 16, 16), cache_size=8)
        self.cm.create_chunk((0, 0, 0))

    def test_world_to_chunk_coords(self):
        self.assertEqual(world_to_chunk_coords(5, 3, 20, (16, 16, 16)), (0, 0, 1))
        self.assertEqual(world_to_chunk_coords(-1, 0, 0, (16, 16, 16)), (-1, 0, 0))

    def test_world_to_local(self):
        self.assertEqual(world_to_local(17, 1, 1, (16, 16, 16)), (1, 1, 1))

    def test_get_block_at_world(self):
        chunk = self.cm.get_chunk((0, 0, 0))
        chunk.set_block_id(2, 3, 4, BLOCK_DIRT)
        self.assertEqual(get_block_id_at_world(self.cm, 2, 3, 4), BLOCK_DIRT)
        self.assertEqual(get_block_id_at_world(self.cm, 99, 0, 0), BLOCK_AIR)

    def test_find_ground_height(self):
        chunk = self.cm.get_chunk((0, 0, 0))
        for y in range(4):
            chunk.set_block_id(0, y, 0, BLOCK_DIRT)
        ground = find_ground_height(self.cm, 0.5, 10.0, 0.5)
        self.assertEqual(ground, 4.0)
        self.assertTrue(is_solid_at_world(self.cm, 0.5, 3.0, 0.5))


if __name__ == "__main__":
    unittest.main()

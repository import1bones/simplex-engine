import unittest

from simplex.ecs.ecs import ECS
from simplex.world.chunk_manager import ChunkManager


class ChunkManagerTests(unittest.TestCase):
    def setUp(self):
        self.ecs = ECS()
        self.cm = ChunkManager(self.ecs, chunk_size=(8, 8, 8), cache_size=2)

    def test_create_and_get_chunk(self):
        ent = self.cm.create_chunk((0, 0, 0))
        self.assertIsNotNone(ent)
        chunk = self.cm.get_chunk((0, 0, 0))
        self.assertIsNotNone(chunk)
        self.assertEqual(len(self.cm.list_loaded()), 1)

    def test_eviction_lru(self):
        # create more chunks than cache_size to force eviction
        self.cm.create_chunk((0, 0, 0))
        self.cm.create_chunk((1, 0, 0))
        # this should push oldest out
        self.cm.create_chunk((2, 0, 0))
        loaded = self.cm.list_loaded()
        self.assertTrue((2, 0, 0) in loaded)
        # one of the earlier ones should be evicted
        self.assertLessEqual(len(loaded), self.cm.cache_size)

    def test_preload_area_and_unload(self):
        self.cm.cache_size = 10
        self.cm.ensure_area_loaded((0, 0, 0), radius=1)
        loaded = set(self.cm.list_loaded())
        # area radius=1 cubic should include (±1) -> at least center present
        self.assertIn((0, 0, 0), loaded)
        # unloading outside area should leave only those within radius
        self.cm.unload_outside_area((0, 0, 0), radius=0)
        loaded2 = set(self.cm.list_loaded())
        self.assertTrue(all(max(abs(x), abs(y), abs(z)) <= 0 for (x, y, z) in loaded2))


if __name__ == "__main__":
    unittest.main()

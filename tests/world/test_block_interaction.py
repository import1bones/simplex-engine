import unittest

from simplex.ecs.block_interaction_system import BlockInteractionSystem
from simplex.ecs.chunk_system import ChunkMeshSystem
from simplex.ecs.components import PositionComponent
from simplex.ecs.ecs import ECS, Entity
from simplex.voxel.voxel import BLOCK_AIR, BLOCK_DIRT
from simplex.world.chunk_manager import ChunkManager
from simplex.world.world_query import (
    get_block_id_at_world,
    raycast_blocks,
    set_block_id_at_world,
    view_direction_from_yaw_pitch,
)


def _clear_chunk(chunk):
    sx, sy, sz = chunk.size
    for x in range(sx):
        for y in range(sy):
            for z in range(sz):
                chunk.set_block_id(x, y, z, BLOCK_AIR)


class RaycastTests(unittest.TestCase):
    def setUp(self):
        self.ecs = ECS()
        self.cm = ChunkManager(self.ecs, chunk_size=(16, 16, 16), cache_size=8)
        self.cm.create_chunk((0, 0, 0))
        _clear_chunk(self.cm.get_chunk((0, 0, 0)))

    def test_view_direction_forward(self):
        dx, dy, dz = view_direction_from_yaw_pitch(0.0, 0.0)
        self.assertAlmostEqual(dx, 0.0, places=3)
        self.assertAlmostEqual(dy, 0.0, places=3)
        self.assertAlmostEqual(dz, 1.0, places=3)

    def test_raycast_hits_solid_block(self):
        chunk = self.cm.get_chunk((0, 0, 0))
        chunk.set_block_id(5, 2, 5, BLOCK_DIRT)
        origin = (5.5, 2.8, 4.5)
        direction = view_direction_from_yaw_pitch(0.0, 0.0)
        result = raycast_blocks(self.cm, origin, direction, max_distance=12.0)
        self.assertTrue(result["hit"])
        self.assertEqual(result["block"], (5, 2, 5))
        self.assertEqual(result["prev"], (5, 2, 4))

    def test_raycast_misses_when_no_solid(self):
        chunk = self.cm.get_chunk((0, 0, 0))
        for x in range(16):
            for z in range(16):
                for y in range(16):
                    chunk.set_block_id(x, y, z, BLOCK_AIR)
        origin = (1.5, 5.0, 1.5)
        direction = view_direction_from_yaw_pitch(0.0, 0.0)
        result = raycast_blocks(self.cm, origin, direction, max_distance=4.0)
        self.assertFalse(result["hit"])

    def test_set_block_marks_chunk_dirty(self):
        entity = self.ecs.get_entity("chunk_0_0_0")
        chunk_comp = entity.get_component("chunk")
        chunk_comp.clear_dirty()

        ok = set_block_id_at_world(self.cm, self.ecs, 3, 1, 3, BLOCK_DIRT)
        self.assertTrue(ok)
        self.assertTrue(chunk_comp.dirty)
        self.assertEqual(get_block_id_at_world(self.cm, 3, 1, 3), BLOCK_DIRT)


class BlockInteractionSystemTests(unittest.TestCase):
    def setUp(self):
        self.ecs = ECS()
        self.cm = ChunkManager(self.ecs, chunk_size=(16, 16, 16), cache_size=8)
        self.cm.create_chunk((0, 0, 0))
        chunk = self.cm.get_chunk((0, 0, 0))
        _clear_chunk(chunk)

        class _Engine:
            pass

        self.engine = _Engine()
        self.engine.ecs = self.ecs
        self.engine.chunk_manager = self.cm

        class _Cam:
            def __init__(self):
                self.position = (5.5, 2.8, 4.5)
                self.yaw = 0.0
                self.pitch = 0.0

        self.engine.camera_follow = _Cam()

        player = Entity("Player")
        player.add_component(PositionComponent(0.0, 4.0, 0.0))
        self.ecs.add_entity(player)

        self.ecs.add_system(ChunkMeshSystem(max_chunks_per_frame=4))
        self.system = BlockInteractionSystem(engine=self.engine)
        self.ecs.add_system(self.system)

    def test_break_block_via_click(self):
        chunk = self.cm.get_chunk((0, 0, 0))
        chunk.set_block_id(5, 2, 5, BLOCK_DIRT)
        entity = self.ecs.get_entity("chunk_0_0_0")
        entity.get_component("chunk").clear_dirty()

        self.system._pending_clicks.append("LEFT")
        self.ecs.update()

        self.assertEqual(get_block_id_at_world(self.cm, 5, 2, 5), BLOCK_AIR)
        self.assertTrue(entity.get_component("chunk").dirty)

    def test_place_block_via_click(self):
        chunk = self.cm.get_chunk((0, 0, 0))
        chunk.set_block_id(5, 0, 5, BLOCK_DIRT)
        self.engine.camera_follow.position = (5.5, 3.0, 5.5)
        self.engine.camera_follow.pitch = -80.0

        entity = self.ecs.get_entity("chunk_0_0_0")
        entity.get_component("chunk").clear_dirty()

        self.system._pending_clicks.append("RIGHT")
        self.ecs.update()

        self.assertEqual(get_block_id_at_world(self.cm, 5, 1, 5), BLOCK_DIRT)
        self.assertTrue(entity.get_component("chunk").dirty)

    def test_remesh_clears_dirty(self):
        chunk = self.cm.get_chunk((0, 0, 0))
        chunk.set_block_id(5, 0, 5, BLOCK_DIRT)
        self.engine.camera_follow.position = (5.5, 3.0, 5.5)
        self.engine.camera_follow.pitch = -80.0

        entity = self.ecs.get_entity("chunk_0_0_0")
        entity.get_component("chunk").clear_dirty()

        self.system._pending_clicks.append("RIGHT")
        self.ecs.update()
        self.assertTrue(entity.get_component("chunk").dirty)

        self.ecs.update()
        self.assertFalse(entity.get_component("chunk").dirty)


if __name__ == "__main__":
    unittest.main()

"""Performance regression tests for voxel ECS update loop.

Measures frame-time jitter without OpenGL so CI stays fast and stable.
Thresholds are relative (spike vs steady-state) to tolerate slow runners.
"""

import statistics
import time
import unittest

from simplex.ecs.chunk_streaming_system import ChunkStreamingSystem
from simplex.ecs.chunk_system import ChunkMeshSystem, ChunkSystem
from simplex.ecs.components import PositionComponent
from simplex.ecs.ecs import ECS, Entity
from simplex.ecs.voxel_collision_system import VoxelCollisionSystem
from simplex.voxel.voxel import BLOCK_DIRT
from simplex.world.chunk_manager import ChunkManager


def _percentile(samples, pct: float) -> float:
    ordered = sorted(samples)
    if not ordered:
        return 0.0
    idx = min(len(ordered) - 1, int(len(ordered) * pct))
    return ordered[idx]


class _VoxelSim:
    """Minimal engine harness: streaming, meshing, and collision without rendering."""

    def __init__(self, mesh_budget: int = 2, streaming_radius: int = 1):
        self.ecs = ECS()
        self.chunk_manager = ChunkManager(
            self.ecs, chunk_size=(16, 16, 16), cache_size=32
        )
        self._last_delta_time = 1.0 / 60.0
        self.ecs.add_system(ChunkSystem())
        self.ecs.add_system(ChunkMeshSystem(max_chunks_per_frame=mesh_budget))
        self.ecs.add_system(
            VoxelCollisionSystem(engine=self),
        )
        self.ecs.add_system(
            ChunkStreamingSystem(
                engine=self,
                radius=streaming_radius,
                horizontal_only=True,
            )
        )
        self.player = Entity("Player")
        self.player.add_component(PositionComponent(0.5, 10.0, 0.5))
        self.ecs.add_entity(self.player)

    def tick(self) -> float:
        start = time.perf_counter()
        self.ecs.update()
        return time.perf_counter() - start

    def warmup(self, max_frames: int = 200) -> None:
        for _ in range(max_frames):
            self.tick()
            if not self._any_dirty_chunks():
                return

    def _any_dirty_chunks(self) -> bool:
        for entity in self.ecs.entities:
            if not entity.name.startswith("chunk_"):
                continue
            chunk_comp = entity.get_component("chunk")
            if chunk_comp and chunk_comp.dirty:
                return True
        return False

    def move_player_to_chunk(self, cx: int, cz: int) -> None:
        pos = self.player.get_component("position")
        pos.x = cx * 16 + 0.5
        pos.z = cz * 16 + 0.5


class PerformanceTests(unittest.TestCase):
    def test_voxel_collision_steady_cost(self):
        sim = _VoxelSim()
        sim.chunk_manager.create_chunk((0, 0, 0))
        chunk = sim.chunk_manager.get_chunk((0, 0, 0))
        for y in range(4):
            chunk.set_block_id(0, y, 0, BLOCK_DIRT)

        samples = [sim.tick() for _ in range(200)]
        median = statistics.median(samples)
        p95 = _percentile(samples, 0.95)
        self.assertLess(median, 0.05, f"collision median too slow: {median:.4f}s")
        self.assertLess(p95, median * 5.0, f"collision jitter: p95={p95:.4f}, median={median:.4f}")

    def test_idle_frame_jitter_after_warmup(self):
        sim = _VoxelSim(mesh_budget=2)
        sim.warmup()
        self.assertFalse(sim._any_dirty_chunks(), "warmup should finish mesh generation")

        samples = [sim.tick() for _ in range(80)]
        median = statistics.median(samples)
        p95 = _percentile(samples, 0.95)
        self.assertLess(p95, max(median * 4.0, 0.002), f"idle jitter: p95={p95:.4f}, median={median:.4f}")

    def test_chunk_boundary_spike_bounded(self):
        sim = _VoxelSim(mesh_budget=2)
        sim.warmup()
        idle = [sim.tick() for _ in range(40)]
        baseline = statistics.median(idle)

        sim.move_player_to_chunk(1, 0)
        boundary_times = [sim.tick() for _ in range(12)]
        spike = max(boundary_times)

        # Mesh budget spreads work; boundary frames should not dwarf steady state.
        self.assertLess(
            spike,
            max(baseline * 10.0, 0.15),
            f"boundary spike={spike:.4f}s vs baseline={baseline:.4f}s",
        )

    def test_mesh_budget_reduces_boundary_spike(self):
        """Tighter mesh budget should keep worst boundary frame closer to idle."""
        loose = _VoxelSim(mesh_budget=9)
        loose.warmup()
        loose.move_player_to_chunk(1, 0)
        loose_spike = max(loose.tick() for _ in range(3))

        tight = _VoxelSim(mesh_budget=1)
        tight.warmup()
        tight.move_player_to_chunk(1, 0)
        tight_spike = max(tight.tick() for _ in range(6))

        self.assertLess(
            tight_spike,
            loose_spike * 1.5 + 0.01,
            f"tight={tight_spike:.4f}s loose={loose_spike:.4f}s",
        )


if __name__ == "__main__":
    unittest.main()

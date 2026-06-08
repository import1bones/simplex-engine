"""World-space block queries via ChunkManager."""

import math
from typing import Tuple

from simplex.voxel.voxel import BLOCK_AIR, is_solid


def world_to_chunk_coords(
    wx: float, wy: float, wz: float, chunk_size: Tuple[int, int, int]
) -> Tuple[int, int, int]:
    sx, sy, sz = chunk_size
    return (
        math.floor(wx / sx),
        math.floor(wy / sy),
        math.floor(wz / sz),
    )


def world_to_local(
    wx: float, wy: float, wz: float, chunk_size: Tuple[int, int, int]
) -> Tuple[int, int, int]:
    sx, sy, sz = chunk_size
    cx, cy, cz = world_to_chunk_coords(wx, wy, wz, chunk_size)
    return (
        int(wx - cx * sx),
        int(wy - cy * sy),
        int(wz - cz * sz),
    )


def get_block_id_at_world(chunk_manager, wx: float, wy: float, wz: float) -> int:
    """Return block id at world coordinates, or air if chunk unloaded."""
    if chunk_manager is None:
        return BLOCK_AIR
    cx, cy, cz = world_to_chunk_coords(wx, wy, wz, chunk_manager.chunk_size)
    chunk = chunk_manager.get_chunk((cx, cy, cz))
    if chunk is None:
        return BLOCK_AIR
    lx, ly, lz = world_to_local(wx, wy, wz, chunk_manager.chunk_size)
    if not chunk.in_bounds(lx, ly, lz):
        return BLOCK_AIR
    return chunk.get_block(lx, ly, lz).block_id


def is_solid_at_world(chunk_manager, wx: float, wy: float, wz: float) -> bool:
    return is_solid(get_block_id_at_world(chunk_manager, wx, wy, wz))


def find_ground_height(
    chunk_manager,
    px: float,
    py: float,
    pz: float,
    half_width: float = 0.3,
    scan_depth: int = 16,
) -> float | None:
    """Highest walkable Y (top of solid + 1) under the player's feet."""
    top = None
    samples = ((px, pz),)
    if half_width > 0:
        samples = (
            (px, pz),
            (px - half_width, pz),
            (px + half_width, pz),
            (px, pz - half_width),
            (px, pz + half_width),
        )
    start_y = int(math.floor(py))
    for wx, wz in samples:
        for y in range(start_y, start_y - scan_depth, -1):
            if is_solid_at_world(chunk_manager, wx, y, wz):
                candidate = float(y + 1)
                top = candidate if top is None else max(top, candidate)
                break
    return top


def feet_on_ground(chunk_manager, px: float, py: float, pz: float) -> bool:
    """Fast check: is there solid directly under the feet?"""
    return is_solid_at_world(chunk_manager, px, py - 0.05, pz)

"""World-space block queries via ChunkManager."""

import math
from typing import Any, Dict, Tuple

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


def view_direction_from_yaw_pitch(yaw_deg: float, pitch_deg: float) -> Tuple[float, float, float]:
    """Unit view vector matching OpenGLRenderer camera (yaw around Y, pitch around X)."""
    yaw_rad = math.radians(yaw_deg)
    pitch_rad = math.radians(pitch_deg)
    fx = math.cos(pitch_rad) * math.sin(yaw_rad)
    fy = math.sin(pitch_rad)
    fz = math.cos(pitch_rad) * math.cos(yaw_rad)
    return (fx, fy, fz)


def _int_bound(s: float, ds: float) -> float:
    if ds == 0:
        return float("inf")
    if ds < 0:
        return (s - math.floor(s)) / -ds
    return (math.floor(s) + 1 - s) / ds


def raycast_blocks(
    chunk_manager,
    origin: Tuple[float, float, float],
    direction: Tuple[float, float, float],
    max_distance: float = 8.0,
) -> Dict[str, Any]:
    """3D DDA grid walk. Returns hit solid block and previous air cell for placement."""
    ox, oy, oz = origin
    dx, dy, dz = direction
    length = math.sqrt(dx * dx + dy * dy + dz * dz)
    if length < 1e-8:
        return {"hit": False}
    dx, dy, dz = dx / length, dy / length, dz / length

    x = int(math.floor(ox))
    y = int(math.floor(oy))
    z = int(math.floor(oz))

    step_x = 1 if dx >= 0 else -1
    step_y = 1 if dy >= 0 else -1
    step_z = 1 if dz >= 0 else -1

    t_delta_x = abs(1 / dx) if dx != 0 else float("inf")
    t_delta_y = abs(1 / dy) if dy != 0 else float("inf")
    t_delta_z = abs(1 / dz) if dz != 0 else float("inf")

    t_max_x = _int_bound(ox, dx)
    t_max_y = _int_bound(oy, dy)
    t_max_z = _int_bound(oz, dz)

    t = 0.0
    prev = (x, y, z)

    while t <= max_distance:
        if is_solid_at_world(chunk_manager, x, y, z):
            return {
                "hit": True,
                "block": (x, y, z),
                "prev": prev,
                "distance": t,
            }
        prev = (x, y, z)

        if t_max_x < t_max_y:
            if t_max_x < t_max_z:
                x += step_x
                t = t_max_x
                t_max_x += t_delta_x
            else:
                z += step_z
                t = t_max_z
                t_max_z += t_delta_z
        elif t_max_y < t_max_z:
            y += step_y
            t = t_max_y
            t_max_y += t_delta_y
        else:
            z += step_z
            t = t_max_z
            t_max_z += t_delta_z

    return {"hit": False}


def mark_chunk_dirty_at_world(chunk_manager, ecs, wx: int, wy: int, wz: int) -> bool:
    """Mark ChunkComponent dirty for the chunk containing world block coords."""
    if chunk_manager is None or ecs is None:
        return False
    cx, cy, cz = world_to_chunk_coords(wx, wy, wz, chunk_manager.chunk_size)
    entity = ecs.get_entity(f"chunk_{cx}_{cy}_{cz}")
    if not entity:
        return False
    chunk_comp = entity.get_component("chunk")
    if chunk_comp:
        chunk_comp.mark_dirty()
        return True
    return False


def set_block_id_at_world(
    chunk_manager,
    ecs,
    wx: int,
    wy: int,
    wz: int,
    block_id: int,
) -> bool:
    """Set block at world integer coords and mark the chunk entity dirty for remesh."""
    if chunk_manager is None:
        return False
    cx, cy, cz = world_to_chunk_coords(wx, wy, wz, chunk_manager.chunk_size)
    chunk = chunk_manager.get_chunk((cx, cy, cz))
    if chunk is None:
        return False
    lx, ly, lz = world_to_local(wx, wy, wz, chunk_manager.chunk_size)
    if not chunk.in_bounds(lx, ly, lz):
        return False
    chunk.set_block_id(lx, ly, lz, block_id)
    return mark_chunk_dirty_at_world(chunk_manager, ecs, wx, wy, wz)


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


def snap_position_to_ground(
    chunk_manager,
    px: float,
    py: float,
    pz: float,
    half_width: float = 0.3,
) -> float | None:
    """Return Y to stand on terrain at (px, pz), or None if no ground loaded."""
    return find_ground_height(chunk_manager, px, py, pz, half_width=half_width)


def feet_on_ground(chunk_manager, px: float, py: float, pz: float) -> bool:
    """Fast check: is there solid directly under the feet?"""
    return is_solid_at_world(chunk_manager, px, py - 0.05, pz)

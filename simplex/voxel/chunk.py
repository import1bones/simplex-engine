"""
Chunk storage for voxel worlds.

This module provides a compact, dependency-light Chunk implementation used
by the early voxel systems. It intentionally avoids numpy for portability
in tests and uses a flat list internally.
"""

from typing import Tuple, List
from .voxel import Voxel, BLOCK_AIR

CHUNK_DEFAULT_SIZE = (16, 16, 16)


class Chunk:
    def __init__(
        self,
        position: Tuple[int, int, int],
        size: Tuple[int, int, int] = CHUNK_DEFAULT_SIZE,
    ):
        self.position = tuple(position)
        self.size = tuple(size)
        self._sx, self._sy, self._sz = self.size
        self._blocks: List[Voxel] = [
            Voxel(BLOCK_AIR) for _ in range(self._sx * self._sy * self._sz)
        ]
        self.dirty = True

    def _index(self, x: int, y: int, z: int) -> int:
        return (x * self._sy * self._sz) + (y * self._sz) + z

    def in_bounds(self, x: int, y: int, z: int) -> bool:
        return 0 <= x < self._sx and 0 <= y < self._sy and 0 <= z < self._sz

    def get_block(self, x: int, y: int, z: int) -> Voxel:
        if not self.in_bounds(x, y, z):
            raise IndexError("Block coordinates out of chunk bounds")
        return self._blocks[self._index(x, y, z)]

    def set_block(self, x: int, y: int, z: int, block: Voxel) -> None:
        if not self.in_bounds(x, y, z):
            raise IndexError("Block coordinates out of chunk bounds")
        self._blocks[self._index(x, y, z)] = block
        self.dirty = True

    def set_block_id(self, x: int, y: int, z: int, block_id: int) -> None:
        self.set_block(x, y, z, Voxel(block_id))

    def iter_blocks(self):
        """Yield (x,y,z, Voxel) for all non-air blocks."""
        for x in range(self._sx):
            for y in range(self._sy):
                for z in range(self._sz):
                    v = self.get_block(x, y, z)
                    if not v.is_air():
                        yield (x, y, z, v)

    def mark_clean(self):
        self.dirty = False

    def is_dirty(self) -> bool:
        return self.dirty

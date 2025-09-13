"""simplex.voxel

Basic voxel primitives and utilities for Simplex Engine.
This package contains lightweight block definitions, chunk storage,
and a naive mesh generator used by early renderer integration.

The code intentionally avoids heavy third-party dependencies so it
can be used in tests and early development. Later we will add
optimized meshers (greedy meshing) and VBO upload helpers.
"""

from .voxel import BLOCK_AIR, Block, PALETTE, is_solid, get_block_color
from .chunk import Chunk
from .meshgen import generate_naive_mesh

__all__ = [
    "BLOCK_AIR",
    "Block",
    "PALETTE",
    "is_solid",
    "get_block_color",
    "Chunk",
    "generate_naive_mesh",
]

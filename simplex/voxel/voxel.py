"""
Voxel/block definition for Minecraft-like worlds.

This module defines a tiny block palette and helpers used by chunk
storage and the mesh generator. Kept minimal so unit tests don't need
heavy deps.
"""

from dataclasses import dataclass

# Block id constants
BLOCK_AIR = 0
BLOCK_DIRT = 1
BLOCK_GRASS = 2
BLOCK_STONE = 3


@dataclass
class BlockDef:
    id: int
    name: str
    solid: bool
    color: tuple


# Small palette
PALETTE = {
    BLOCK_AIR: BlockDef(BLOCK_AIR, "air", False, (0.0, 0.0, 0.0, 0.0)),
    BLOCK_DIRT: BlockDef(
        BLOCK_DIRT, "dirt", True, (134 / 255, 96 / 255, 67 / 255, 1.0)
    ),
    BLOCK_GRASS: BlockDef(
        BLOCK_GRASS, "grass", True, (106 / 255, 190 / 255, 92 / 255, 1.0)
    ),
    BLOCK_STONE: BlockDef(
        BLOCK_STONE, "stone", True, (120 / 255, 120 / 255, 120 / 255, 1.0)
    ),
}


def is_solid(block_id: int) -> bool:
    return PALETTE.get(block_id, PALETTE[BLOCK_AIR]).solid


def get_block_color(block_id: int) -> tuple:
    return PALETTE.get(block_id, PALETTE[BLOCK_AIR]).color


class Voxel:
    """Simple voxel container used by chunk storage.

    Kept tiny: stores block_id and optional metadata dict.
    """

    def __init__(self, block_id=BLOCK_AIR, data=None):
        self.block_id = int(block_id)
        self.data = data or {}

    def is_air(self):
        return self.block_id == BLOCK_AIR


# Provide legacy name expected by imports
Block = BlockDef

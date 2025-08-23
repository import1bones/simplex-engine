"""
Chunk data structure for Minecraft-like voxel worlds.
"""
import numpy as np
from .voxel import Voxel

CHUNK_SIZE_X = 16
CHUNK_SIZE_Y = 64  # You can increase to 256 for full scale
CHUNK_SIZE_Z = 16

class Chunk:
    def __init__(self, position):
        self.position = position  # (chunk_x, chunk_y, chunk_z)
        self.blocks = np.zeros((CHUNK_SIZE_X, CHUNK_SIZE_Y, CHUNK_SIZE_Z), dtype=np.uint8)
        # Optionally: store Voxel objects or just block IDs for performance

    def get_block(self, x, y, z):
        return self.blocks[x, y, z]

    def set_block(self, x, y, z, block_id):
        self.blocks[x, y, z] = block_id

"""
Voxel/block definition for Minecraft-like worlds.
"""

class Voxel:
    def __init__(self, block_id=0, data=None):
        self.block_id = block_id  # 0=air, 1=stone, 2=grass, etc.
        self.data = data or {}

    def is_air(self):
        return self.block_id == 0

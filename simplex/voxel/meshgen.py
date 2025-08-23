"""
Chunk mesh generation for OpenGL rendering.
"""
import numpy as np
from .chunk import CHUNK_SIZE_X, CHUNK_SIZE_Y, CHUNK_SIZE_Z

def greedy_mesh(chunk):
    # Placeholder: naive mesh (one cube per block, no face culling)
    vertices = []
    colors = []
    for x in range(CHUNK_SIZE_X):
        for y in range(CHUNK_SIZE_Y):
            for z in range(CHUNK_SIZE_Z):
                block_id = chunk.get_block(x, y, z)
                if block_id != 0:
                    # Add a cube at (x, y, z)
                    vertices.append((x, y, z))
                    colors.append(block_id)
    return vertices, colors

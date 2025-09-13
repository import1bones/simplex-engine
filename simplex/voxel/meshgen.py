"""
Naive mesh generator for Chunk data.

Produces a list of quads (as 6-vertex triangles) suitable for a simple
immediate-mode renderer. This is a reference implementation used in
unit tests and early renderer integration.
"""

from typing import List, Tuple
from .voxel import is_solid, get_block_color, BLOCK_AIR


# Cube faces with vertex offsets (each face is two triangles, 6 vertices)
_FACE_DELTAS = {
    "px": [((1, 0, 0), (1, 1, 0), (1, 1, 1), (1, 0, 1))],
    "nx": [((0, 0, 1), (0, 1, 1), (0, 1, 0), (0, 0, 0))],
    "py": [((0, 1, 0), (1, 1, 0), (1, 1, 1), (0, 1, 1))],
    "ny": [((0, 0, 1), (1, 0, 1), (1, 0, 0), (0, 0, 0))],
    "pz": [((0, 0, 0), (0, 1, 0), (1, 1, 0), (1, 0, 0))],
    "nz": [((1, 0, 1), (1, 1, 1), (0, 1, 1), (0, 0, 1))],
}

# For each face we provide two triangles (as indices into the quad)
_TRI_IDX = [(0, 1, 2), (0, 2, 3)]


def generate_naive_mesh(chunk) -> Tuple[List[float], List[float]]:
    """Generate a naive mesh for the given chunk.

    Returns (vertices, colors) where vertices is a flat list of floats
    (x,y,z) per vertex and colors is a matching flat list of floats
    (r,g,b,a) per vertex.
    """
    verts: List[float] = []
    cols: List[float] = []

    sx, sy, sz = chunk.size

    for x in range(sx):
        for y in range(sy):
            for z in range(sz):
                v = chunk.get_block(x, y, z)
                if v.is_air():
                    continue
                bid = v.block_id
                color = get_block_color(bid)
                # For each face, check neighbor; if neighbor is air, emit face
                neighbors = [
                    (x + 1, y, z, "px"),
                    (x - 1, y, z, "nx"),
                    (x, y + 1, z, "py"),
                    (x, y - 1, z, "ny"),
                    (x, y, z + 1, "pz"),
                    (x, y, z - 1, "nz"),
                ]
                for nx, ny, nz, face_key in neighbors:
                    if 0 <= nx < sx and 0 <= ny < sy and 0 <= nz < sz:
                        n = chunk.get_block(nx, ny, nz)
                        if not n.is_air():
                            continue
                    # neighbor out of bounds is treated as air
                    # emit quad for this face
                    quad = _FACE_DELTAS[face_key][0]
                    for tri in _TRI_IDX:
                        for idx in tri:
                            ox, oy, oz = quad[idx]
                            vx = x + ox
                            vy = y + oy
                            vz = z + oz
                            verts.extend([vx, vy, vz])
                            cols.extend(list(color))

    return verts, cols

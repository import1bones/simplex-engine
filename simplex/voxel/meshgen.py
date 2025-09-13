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


def generate_greedy_mesh(chunk) -> Tuple[List[float], List[float]]:
    """Greedy meshing implementation adapted for axis-aligned block grids.

    Produces the same output format as generate_naive_mesh (flat vertex and
    color lists) but merges adjacent faces into larger quads to significantly
    reduce vertex count. This implementation follows the standard 3-pass
    greedy meshing algorithm (one pass per axis).
    """
    verts: List[float] = []
    cols: List[float] = []

    sx, sy, sz = chunk.size

    # Helper to safely get block id at coords, returns 0 for air/out-of-bounds
    def _block_id(x, y, z):
        if 0 <= x < sx and 0 <= y < sy and 0 <= z < sz:
            v = chunk.get_block(x, y, z)
            return 0 if v.is_air() else v.block_id
        return 0

    # For each principal axis (0=x,1=y,2=z)
    for d in range(3):
        u = (d + 1) % 3
        v = (d + 2) % 3
        dims = [sx, sy, sz]
        du = dims[u]
        dv = dims[v]
        dd = dims[d]

        # Iterate through slices perpendicular to axis d
        for q in range(dd + 1):
            # Build mask of size du * dv
            mask = [0] * (du * dv)
            for i in range(du):
                for j in range(dv):
                    # coordinates for cell on side q-1 (a) and q (b)
                    a = [0, 0, 0]
                    b = [0, 0, 0]
                    a[d] = q - 1
                    b[d] = q
                    a[u] = i
                    b[u] = i
                    a[v] = j
                    b[v] = j
                    ida = _block_id(a[0], a[1], a[2])
                    idb = _block_id(b[0], b[1], b[2])
                    # face exists when one side is filled and other empty
                    if ida != 0 and idb == 0:
                        mask[i + j * du] = ida  # front face
                    elif ida == 0 and idb != 0:
                        mask[i + j * du] = -idb  # back face (negative marker)
                    else:
                        mask[i + j * du] = 0

            # Greedy merge on mask
            i = 0
            while i < du:
                j = 0
                while j < dv:
                    idx = i + j * du
                    mval = mask[idx]
                    if mval == 0:
                        j += 1
                        continue
                    # compute width
                    w = 1
                    while i + w < du and mask[(i + w) + j * du] == mval:
                        w += 1
                    # compute height
                    h = 1
                    done = False
                    while j + h < dv and not done:
                        for k in range(w):
                            if mask[(i + k) + (j + h) * du] != mval:
                                done = True
                                break
                        if not done:
                            h += 1
                    # Emit quad for this run
                    # base coordinate in 3D
                    base = [0.0, 0.0, 0.0]
                    base[d] = float(q) if mval > 0 else float(q)  # plane position
                    base[u] = float(i)
                    base[v] = float(j)

                    # Depending on sign, face is on + or - side of voxel
                    sign = 1 if mval > 0 else -1
                    block_id = abs(mval)
                    color = get_block_color(block_id)

                    # Compute four corners of the quad in world space
                    # Corners are ordered to form two triangles
                    # We need to map (du, dv) extents into (x,y,z)
                    # corner offsets (0,0), (w,0), (w,h), (0,h)
                    def _corner(off_u, off_v):
                        c = [0.0, 0.0, 0.0]
                        c[d] = base[d]
                        c[u] = base[u] + off_u
                        c[v] = base[v] + off_v
                        # shift face along normal if front face so it sits on voxel face
                        if mval > 0:
                            # front face corresponds to side where a was filled and b empty -> at q
                            c[d] = float(q)
                        else:
                            # back face corresponds to side where b was filled -> at q
                            c[d] = float(q)
                        return tuple(c)

                    c0 = _corner(0, 0)
                    c1 = _corner(w, 0)
                    c2 = _corner(w, h)
                    c3 = _corner(0, h)

                    # For correct winding, flip order for back faces
                    if mval > 0:
                        quad_verts = [c0, c1, c2, c3]
                    else:
                        quad_verts = [c1, c0, c3, c2]

                    # Emit two triangles
                    for tri in [(0, 1, 2), (0, 2, 3)]:
                        for idx_tri in tri:
                            vx, vy, vz = quad_verts[idx_tri]
                            verts.extend([vx, vy, vz])
                            cols.extend(list(color))

                    # Zero out mask for covered area
                    for jj in range(h):
                        for ii in range(w):
                            mask[(i + ii) + (j + jj) * du] = 0

                    # advance
                    j += h
                i += 1

    return verts, cols

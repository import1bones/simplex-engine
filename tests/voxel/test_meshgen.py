from simplex.voxel.chunk import Chunk
from simplex.voxel.meshgen import generate_naive_mesh
from simplex.voxel.voxel import BLOCK_DIRT


def test_meshgen_emits_faces_for_single_block():
    c = Chunk((0, 0, 0), size=(3, 3, 3))
    c.set_block_id(1, 1, 1, BLOCK_DIRT)
    verts, cols = generate_naive_mesh(c)
    # A single isolated block should produce 6 faces * 2 triangles * 3 vertices = 36 vertices
    assert len(verts) == 36 * 3
    assert len(cols) == 36 * 4


def test_meshgen_ignores_interior_faces():
    c = Chunk((0, 0, 0), size=(3, 3, 3))
    # place two adjacent blocks; internal faces should be culled
    c.set_block_id(1, 1, 1, BLOCK_DIRT)
    c.set_block_id(2, 1, 1, BLOCK_DIRT)
    verts, cols = generate_naive_mesh(c)
    # two-block column: expected faces = (6 + 5) * 2 triangles * 3 verts = fewer than 72
    assert len(verts) < 72 * 3

from simplex.voxel.chunk import Chunk
from simplex.voxel.voxel import BLOCK_DIRT
from simplex.voxel.meshgen import generate_naive_mesh, generate_greedy_mesh


def test_greedy_reduces_vertices_flat_plane():
    c = Chunk((0,0,0), size=(8,4,8))
    # Fill a flat layer at y=0
    for x in range(8):
        for z in range(8):
            c.set_block_id(x,0,z,BLOCK_DIRT)

    naive_verts, _ = generate_naive_mesh(c)
    greedy_verts, _ = generate_greedy_mesh(c)

    assert len(greedy_verts) < len(naive_verts)


def test_greedy_matches_naive_for_single_block():
    c = Chunk((0,0,0), size=(3,3,3))
    c.set_block_id(1,1,1,BLOCK_DIRT)
    naive_verts, naive_cols = generate_naive_mesh(c)
    greedy_verts, greedy_cols = generate_greedy_mesh(c)
    assert len(naive_verts) == len(greedy_verts)
    assert naive_cols == greedy_cols

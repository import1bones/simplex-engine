import pytest

from simplex.voxel.chunk import Chunk
from simplex.voxel.voxel import BLOCK_AIR, BLOCK_DIRT


def test_chunk_get_set_and_iter():
    c = Chunk((0, 0, 0), size=(4, 4, 4))

    # Initially all air
    with pytest.raises(IndexError):
        c.get_block(10, 0, 0)

    # Set a block and retrieve it
    c.set_block_id(1, 2, 3, BLOCK_DIRT)
    v = c.get_block(1, 2, 3)
    assert v.block_id == BLOCK_DIRT
    assert not v.is_air()

    # iter_blocks should yield our set block
    found = list(c.iter_blocks())
    assert any(x == 1 and y == 2 and z == 3 for (x, y, z, _v) in found)


def test_chunk_bounds_checking():
    c = Chunk((0, 0, 0), size=(2, 2, 2))
    with pytest.raises(IndexError):
        c.set_block_id(-1, 0, 0, BLOCK_DIRT)
    with pytest.raises(IndexError):
        c.set_block_id(2, 0, 0, BLOCK_DIRT)

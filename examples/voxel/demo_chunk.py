"""Simple demo: spawn a chunk entity and run a few update frames so ChunkSystem
and ChunkMeshSystem generate a mesh that the renderer can draw.

Run with:

PYTHONPATH=. python3 examples/voxel/demo_chunk.py

This will open the renderer window if OpenGL/pygame are available.
"""

from time import sleep

from simplex.engine import Engine
from simplex.ecs.ecs import Entity
from simplex.ecs.components import ChunkComponent
from simplex.utils.logger import log


def main():
    engine = Engine()

    # Create an entity that will hold a chunk at chunk coordinates (0,0,0)
    e = Entity("chunk_0_0_0")
    chunk_comp = ChunkComponent(position=(0, 0, 0), size=(8, 8, 8))
    e.add_component(chunk_comp)
    engine.ecs.add_entity(e)

    try:
        log("Starting demo loop (3 frames)", level="INFO")
        for i in range(3):
            engine.update()
            sleep(0.1)
    finally:
        engine.shutdown()


if __name__ == "__main__":
    main()

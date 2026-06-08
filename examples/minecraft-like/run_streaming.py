"""Streaming demo: loads an area around a moving center and forces eviction.

This demo sets a small cache_size so eviction happens quickly and demonstrates
ChunkManager.preload_area and unload_outside_area.
"""

import sys
import os
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from simplex.engine import Engine


def main():
    engine = Engine()

    # Replace chunk manager with a small cache to force eviction
    if hasattr(engine, 'chunk_manager') and engine.chunk_manager is not None:
        engine.chunk_manager.cache_size = 3

    centers = [(0,0,0), (1,0,0), (2,0,0), (3,0,0)]

    try:
        for i, c in enumerate(centers):
            print(f"Step {i}: ensuring area around {c}")
            if engine.chunk_manager:
                engine.chunk_manager.ensure_area_loaded(c, radius=0)
                print(f"Loaded: {engine.chunk_manager.list_loaded()}")
            # Run a frame so chunk systems may generate meshes
            engine.update()
            time.sleep(0.1)
    finally:
        engine.shutdown()


if __name__ == '__main__':
    main()

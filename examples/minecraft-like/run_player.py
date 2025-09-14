"""Player demo: spawn a player entity and attach camera follow; use WASD input.

Run this demo and press WASD/SPACE to move. Camera follows player.
"""

import sys
import os
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from simplex.engine import Engine


def main():
    engine = Engine()

    player = engine.spawn_player(position=(8, 8, 8))
    # Ensure a chunk around player exists
    if hasattr(engine, 'chunk_manager') and engine.chunk_manager is not None:
        engine.chunk_manager.ensure_area_loaded((0,0,0), radius=1)

    try:
        print("Player demo: move with WASD, Space to go up. Running 200 frames or exit with Ctrl-C")
        for i in range(200):
            engine.update()
            time.sleep(0.02)
    finally:
        engine.shutdown()


if __name__ == '__main__':
    main()

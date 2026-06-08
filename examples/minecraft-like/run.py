"""Run a minimal Minecraft-like demo using simplex-engine.

This script uses Engine.spawn_chunk and Engine.set_camera to create a simple scene
and runs a few frames so that chunk mesh generation occurs and renderer draws.
"""

import sys
import os
# Ensure repository root is on sys.path so examples can be executed directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from time import sleep

from simplex.engine import Engine


class Camera:
    def __init__(self, position=(16, 16, 48), target=(16, 16, 0)):
        self.position = position
        self.target = target


def main():
    engine = Engine()

    # Attach camera to renderer
    cam = Camera()
    engine.set_camera(cam)

    # Spawn a chunk at origin
    engine.spawn_chunk(position=(0, 0, 0), size=(8, 8, 8))

    try:
        print("Running demo loop (5 frames)")
        for i in range(5):
            engine.update()
            sleep(0.1)
    finally:
        engine.shutdown()


if __name__ == "__main__":
    main()

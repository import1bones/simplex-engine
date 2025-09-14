#!/usr/bin/env python3
"""Minimal Minecraft-like run script for manual playtesting.
Spawns player, sets camera, streams few chunks, runs a short loop rendering frames.
"""

import sys
import os
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from simplex.engine import Engine


def main():
    eng = Engine()

    # Spawn player and set camera
    player = eng.spawn_player('Player', position=(0, 2, 0))
    if player:
        eng.set_camera(eng.camera_follow)

    # Spawn some nearby chunks
    for x in range(-1, 2):
        for z in range(-1, 2):
            eng.spawn_chunk(position=(x * 16, 0, z * 16))

    # Run a few update/render cycles
    for i in range(60):
        eng.update(1.0 / 60.0)
        time.sleep(1.0 / 60.0)

    eng.shutdown()


if __name__ == '__main__':
    main()

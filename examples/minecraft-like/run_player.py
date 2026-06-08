#!/usr/bin/env python3
"""Interactive Minecraft-like player demo.

Spawns a player, loads nearby chunks, and runs until the window is closed.
Controls: WASD move, mouse look, Space up, ESC toggle mouse capture.
"""

import sys
import os
import time

# Relaunch under XWayland once when on Wayland so SDL window mapping is reliable.
if (
    os.environ.get("WAYLAND_DISPLAY")
    and os.environ.get("SDL_VIDEODRIVER") != "x11"
    and os.environ.get("SIMPLEX_XWAYLAND_RELAUNCHED") != "1"
):
    print("Wayland detected — relaunching with SDL_VIDEODRIVER=x11...")
    new_env = dict(os.environ)
    new_env["SDL_VIDEODRIVER"] = "x11"
    new_env["SIMPLEX_XWAYLAND_RELAUNCHED"] = "1"
    try:
        os.execve(sys.executable, [sys.executable] + sys.argv, new_env)
    except Exception as e:
        print("Failed to relaunch under XWayland:", e)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from simplex.engine import Engine


def main():
    eng = Engine()

    player = eng.spawn_player("Player", position=(0, 5, 0))
    if player:
        eng.set_camera(eng.camera_follow)

    for x in range(-1, 2):
        for z in range(-1, 2):
            eng.spawn_chunk(position=(x, 0, z))

    # Prime a few frames so chunk meshes are generated before the interactive loop.
    for _ in range(3):
        eng.update(1.0 / 60.0)

    try:
        import pygame

        clock = pygame.time.Clock()
    except Exception:
        clock = None

    try:
        while True:
            eng.update(1.0 / 60.0)
            ogl = eng.get_opengl_renderer()
            if ogl is not None and not getattr(ogl, "initialized", True):
                break
            if clock:
                clock.tick(60)
            else:
                time.sleep(1.0 / 60.0)
    except KeyboardInterrupt:
        pass
    finally:
        eng.shutdown()


if __name__ == "__main__":
    main()

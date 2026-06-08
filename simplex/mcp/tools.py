"""Headless tool implementations for the simplex MCP server."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parents[2]


def repo_root() -> Path:
    return _REPO_ROOT


def project_status() -> dict[str, Any]:
    """Return repository and test-suite snapshot."""
    status: dict[str, Any] = {
        "name": "simplex-engine",
        "root": str(_REPO_ROOT),
        "python": sys.version.split()[0],
    }

    try:
        import simplex

        status["package"] = getattr(simplex, "__version__", "0.0.1")
    except Exception as exc:
        status["package_error"] = str(exc)

    branch = _git(["rev-parse", "--abbrev-ref", "HEAD"])
    if branch:
        status["branch"] = branch
    dirty = _git(["status", "--porcelain"])
    status["clean"] = dirty == "" or dirty is None
    if dirty:
        status["dirty_files"] = [
            line[3:] for line in dirty.splitlines() if len(line) > 3
        ]

    test_count = _count_tests()
    if test_count is not None:
        status["test_count"] = test_count

    return status


def engine_capabilities() -> dict[str, Any]:
    """Describe implemented engine subsystems for AI planners."""
    return {
        "architecture": "ECS + event-driven subsystems",
        "rendering": {
            "backends": ["opengl", "simple_renderer (2D pygame)"],
            "voxel": ["greedy_mesh", "naive_mesh", "vbo_upload", "ecs_mesh_draw"],
        },
        "world": {
            "chunk_manager": True,
            "streaming": "horizontal player-driven with hysteresis",
            "collision": "voxel grid gravity and horizontal blocking",
        },
        "demos": list_demos(),
        "config_path": "examples/config.toml",
        "test_command": "uv run pytest tests/ -q",
        "lint_command": "uv run ruff check simplex/ tests/",
    }


def list_demos() -> list[dict[str, str]]:
    """List runnable example entry points."""
    demos = [
        {
            "name": "minecraft_player",
            "path": "examples/minecraft-like/run_player.py",
            "description": "First-person voxel demo with streaming and collision",
        },
        {
            "name": "minecraft_basic",
            "path": "examples/minecraft-like/run.py",
            "description": "Single-chunk render smoke test",
        },
        {
            "name": "ping_pong_simple",
            "path": "examples/ping_pong/run_simple.py",
            "description": "2D ping-pong with AI opponent",
        },
        {
            "name": "ping_pong_gui",
            "path": "examples/ping_pong/main_gui.py",
            "description": "Full ping-pong ECS + GUI demo",
        },
    ]
    return [d for d in demos if (_REPO_ROOT / d["path"]).exists()]


def run_command(
    args: list[str],
    *,
    cwd: Path | None = None,
    timeout: int = 300,
) -> dict[str, Any]:
    """Run a subprocess and capture result."""
    try:
        proc = subprocess.run(
            args,
            cwd=cwd or _REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return {
            "command": args,
            "exit_code": proc.returncode,
            "stdout": proc.stdout[-12000:],
            "stderr": proc.stderr[-12000:],
            "success": proc.returncode == 0,
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "command": args,
            "exit_code": -1,
            "success": False,
            "error": f"timeout after {timeout}s",
            "stdout": (exc.stdout or "")[-4000:] if exc.stdout else "",
            "stderr": (exc.stderr or "")[-4000:] if exc.stderr else "",
        }
    except Exception as exc:
        return {
            "command": args,
            "exit_code": -1,
            "success": False,
            "error": str(exc),
        }


def run_tests(path: str = "tests/", extra_args: str = "") -> dict[str, Any]:
    """Run pytest via uv."""
    args = ["uv", "run", "pytest", path, "-q", "--tb=short"]
    if extra_args.strip():
        args.extend(extra_args.split())
    return run_command(args)


def run_lint() -> dict[str, Any]:
    """Run ruff on core packages."""
    return run_command(["uv", "run", "ruff", "check", "simplex/", "tests/"])


def world_probe(
    x: float = 0.0,
    y: float = 8.0,
    z: float = 0.0,
    radius: int = 1,
) -> dict[str, Any]:
    """Headless chunk/world snapshot without opening a display."""
    from simplex.ecs.chunk_streaming_system import ChunkStreamingSystem
    from simplex.ecs.components import PositionComponent
    from simplex.ecs.ecs import ECS, Entity
    from simplex.world.chunk_manager import ChunkManager
    from simplex.world.world_query import feet_on_ground, find_ground_height

    ecs = ECS()
    cm = ChunkManager(ecs, chunk_size=(16, 16, 16), cache_size=32)

    class _Engine:
        pass

    engine = _Engine()
    engine.ecs = ecs
    engine.chunk_manager = cm

    streaming = ChunkStreamingSystem(
        engine=engine, radius=radius, horizontal_only=True
    )
    player = Entity("Player")
    player.add_component(PositionComponent(x, y, z))
    ecs.add_entity(player)

    streaming._process_entities(ecs.entities)
    cm.ensure_area_loaded(streaming._last_center or (0, 0, 0), radius=radius, horizontal_only=True)

    loaded = sorted(cm.list_loaded())
    ground = find_ground_height(cm, x, y, z)
    on_ground = feet_on_ground(cm, x, y, z)

    return {
        "player": {"x": x, "y": y, "z": z},
        "stream_center": streaming._last_center,
        "loaded_chunks": [list(c) for c in loaded],
        "loaded_count": len(loaded),
        "ground_y": ground,
        "on_ground": on_ground,
    }


def read_resource(relative_path: str) -> str:
    """Read a text file from the repository."""
    path = (_REPO_ROOT / relative_path).resolve()
    if not path.is_relative_to(_REPO_ROOT):
        raise ValueError(f"Path escapes repository: {relative_path}")
    if not path.exists():
        raise FileNotFoundError(relative_path)
    return path.read_text(encoding="utf-8")


def _git(args: list[str]) -> str | None:
    try:
        proc = subprocess.run(
            ["git", *args],
            cwd=_REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        if proc.returncode != 0:
            return None
        return proc.stdout.strip()
    except Exception:
        return None


def _count_tests() -> int | None:
    result = run_command(
        ["uv", "run", "pytest", "tests/", "--collect-only", "-q"],
        timeout=60,
    )
    if not result.get("success"):
        return None
    count = 0
    for line in result.get("stdout", "").splitlines():
        if " test" in line and " in " in line:
            try:
                count = int(line.split()[0])
            except ValueError:
                pass
    return count or None

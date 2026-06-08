"""MCP server exposing simplex-engine tools and resources to AI clients."""

from __future__ import annotations

import json

from mcp.server.fastmcp import FastMCP

from . import tools

mcp = FastMCP(
    "simplex-engine",
    instructions=(
        "MCP server for simplex-engine (Python ECS voxel game engine). "
        "Read AGENTS.md via agent_instructions or simplex://agents. "
        "Use health_check before PRs; world_probe for headless voxel state; "
        "good_first_issues for contributor tasks. Demos need a display except world_probe."
    ),
)


@mcp.tool()
def project_status() -> str:
    """Git branch, cleanliness, Python version, and collected test count."""
    return json.dumps(tools.project_status(), indent=2)


@mcp.tool()
def engine_capabilities() -> str:
    """Implemented subsystems, demos, and common commands."""
    return json.dumps(tools.engine_capabilities(), indent=2)


@mcp.tool()
def list_demos() -> str:
    """Runnable example scripts with paths and descriptions."""
    return json.dumps(tools.list_demos(), indent=2)


@mcp.tool()
def run_tests(path: str = "tests/", extra_args: str = "") -> str:
    """Run pytest (default: all tests under tests/)."""
    return json.dumps(tools.run_tests(path=path, extra_args=extra_args), indent=2)


@mcp.tool()
def run_lint() -> str:
    """Run ruff on simplex/ and tests/."""
    return json.dumps(tools.run_lint(), indent=2)


@mcp.tool()
def agent_instructions() -> str:
    """Agent onboarding: commands, MVP priorities, MCP tool list. See AGENTS.md."""
    return json.dumps(tools.agent_instructions(), indent=2)


@mcp.tool()
def health_check() -> str:
    """Pre-PR check: run ruff and full pytest suite."""
    return json.dumps(tools.health_check(), indent=2)


@mcp.tool()
def good_first_issues() -> str:
    """Scoped contributor tasks from GOOD_FIRST_ISSUES.md."""
    return tools.good_first_issues()


@mcp.tool()
def demo_instructions(name: str = "minecraft_player") -> str:
    """Run command and controls for a demo (minecraft_player, ping_pong_simple, etc.)."""
    return json.dumps(tools.demo_instructions(name=name), indent=2)


@mcp.tool()
def world_probe(
    x: float = 0.0,
    y: float = 8.0,
    z: float = 0.0,
    radius: int = 1,
) -> str:
    """Headless voxel probe: loaded chunks, stream center, ground height (no GPU)."""
    return json.dumps(
        tools.world_probe(x=x, y=y, z=z, radius=radius),
        indent=2,
    )


@mcp.resource("simplex://agents")
def resource_agents() -> str:
    """AI agent guide (AGENTS.md)."""
    return tools.read_resource("AGENTS.md")


@mcp.resource("simplex://contributing")
def resource_contributing() -> str:
    """Contributor guide (CONTRIBUTING.md)."""
    return tools.read_resource("CONTRIBUTING.md")


@mcp.resource("simplex://good-first-issues")
def resource_good_first_issues() -> str:
    """Good first issues list."""
    return tools.read_resource("GOOD_FIRST_ISSUES.md")


@mcp.resource("simplex://docs/todo")
def resource_todo() -> str:
    """Project TODO list."""
    return tools.read_resource("docs/todo/todo.md")


@mcp.resource("simplex://config")
def resource_config() -> str:
    """Default engine config (examples/config.toml)."""
    return tools.read_resource("examples/config.toml")


@mcp.resource("simplex://readme")
def resource_readme() -> str:
    """Repository README."""
    return tools.read_resource("README.md")


@mcp.resource("simplex://architecture")
def resource_architecture() -> str:
    """High-level engine architecture notes."""
    return tools.read_resource("docs/development/architecture/current-architecture.md")


def create_server() -> FastMCP:
    return mcp


def smoke_check() -> int:
    """Verify MCP tools work without starting the stdio protocol loop."""
    status = tools.project_status()
    probe = tools.world_probe()
    print("simplex-mcp OK")
    print(f"  root: {status['root']}")
    print(f"  branch: {status.get('branch', 'unknown')}")
    print(f"  tests: {status.get('test_count', '?')}")
    print(f"  loaded_chunks: {probe['loaded_count']}")
    return 0


def main() -> None:
    import sys

    if "--help" in sys.argv or "-h" in sys.argv:
        print("Usage: simplex-mcp          # stdio MCP server (started by Cursor)")
        print("       simplex-mcp --check  # smoke test, no stdio protocol")
        return

    if "--check" in sys.argv:
        raise SystemExit(smoke_check())

    # Stdio transport expects JSON-RPC from an MCP client, not a human terminal.
    if sys.stdin.isatty():
        print(
            "simplex-mcp listens on stdin for MCP clients (Cursor), "
            "not interactive terminal input."
        )
        print("  Smoke test:  uv run simplex-mcp --check")
        print("  Enable in:   Cursor Settings → MCP → simplex-engine")
        raise SystemExit(0)

    mcp.run()


if __name__ == "__main__":
    main()

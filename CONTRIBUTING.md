# Contributing to simplex-engine

Thank you for helping build a simple, AI-friendly Python game engine.

## Quick start

```bash
git clone https://github.com/import1bones/simplex-engine.git
cd simplex-engine
uv sync
uv run pytest tests/ -q
uv run simplex-mcp --check
```

## AI-assisted workflow

1. Enable **simplex-engine** MCP in Cursor (see `docs/advanced/ai/README.md`).
2. Read **AGENTS.md** for agent conventions.
3. Pick a task from **GOOD_FIRST_ISSUES.md**.
4. Ask your agent to run `health_check` before opening a PR.

## Making changes

1. Create a branch from `main`.
2. Keep PRs small and focused.
3. Match existing code style (ruff enforces basics).
4. Add tests for behavior you introduce or fix.
5. Run:

```bash
uv run ruff check simplex/ tests/
uv run pytest tests/ -q
```

## Project layout

- `simplex/` — engine library
- `examples/` — runnable demos (not collected by pytest)
- `tests/` — unit and integration tests
- `docs/` — human documentation
- `simplex/mcp/` — MCP server for AI tools

## Pull requests

- Target `main`
- Describe **why** the change is needed
- Note manual testing (e.g. `run_player.py`) when touching gameplay
- CI must pass (ruff + pytest on Ubuntu with xvfb)

## Questions

Open a GitHub issue or discussion. Include output of `uv run simplex-mcp --check` when reporting environment problems.

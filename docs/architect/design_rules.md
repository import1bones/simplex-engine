# Design & Implementation Rules for simplex-engine

## Code Style
- Follow PEP8 for Python code formatting and naming conventions.
- Use type hints for all public methods and functions.
- Write clear, concise docstrings for all classes, methods, and modules.
- Prefer explicit over implicit code; avoid magic numbers and hardcoded values.
- Organize code into logical modules and packages reflecting architecture.

## Design Style
- Use interfaces (abstract base classes) for all subsystems to enable easy replacement and extension.
- Favor composition over inheritance for game objects and systems.
- Keep subsystems loosely coupled; communicate via well-defined interfaces.
- Design for testability: write small, focused classes and functions.
- Document all public APIs and architectural decisions.

## Achieving Maintainability
- Write unit tests for all core logic and interfaces.
- Use clear separation of concerns: ECS, Renderer, Physics, Scripting, Resource Manager, Audio.
- Avoid circular dependencies between modules.
- Refactor code regularly to improve readability and structure.
- Maintain up-to-date documentation for code and architecture.

## Achieving Flexibility
- Make all subsystems pluggable via interfaces; allow users to swap implementations.
- Support configuration via external files (e.g., JSON, YAML, TOML) for engine settings.
- Use event-driven patterns for extensibility (e.g., ECS event system).
- Allow hot-reloading for scripts and assets where possible.
- Design APIs to be forward-compatible for future features.

## Feature Development
- Start with MVP features; add advanced features incrementally.
- Prototype new features in isolation before integrating into the main codebase.
- Review and discuss architecture decisions before major changes.
- Ensure new features do not break existing functionality or interfaces.

---
Follow these rules to ensure simplex-engine remains maintainable, flexible, and easy to extend as it grows.

# Design & Implementation Rules for simplex-engine

## Code Style
- Follow PEP8 for Python code formatting and naming conventions.
- Use type hints for all public methods and functions.
- Write clear, concise docstrings for all classes, methods, and modules.
- Prefer explicit over implicit code; avoid magic numbers and hardcoded values.
- Organize code into logical modules and packages reflecting architecture.



## Observability

- Ensure all subsystems and resource types provide clear, consistent, and actionable logging for key operations, errors, and state changes.
- Use the engine's logging system for all status, error, and debug messages to support troubleshooting, monitoring, and system transparency.
- Design for runtime observability: make it easy to trace, audit, and understand system behavior through logs and events.

## Design Style

- Use interfaces (abstract base classes, via Python's `abc` module) for all subsystems to enable easy replacement, extension, and contract enforcement.
- Favor composition over inheritance for game objects and systems.
- Keep subsystems loosely coupled; communicate via well-defined interfaces and the event system. Avoid direct dependencies between subsystems.
- Design for testability: write small, focused classes and functions. Mock dependencies in tests.
- Document all public APIs, expected behaviors, and architectural decisions.
- Implement a logging system with multiple levels (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL) to support troubleshooting and root cause analysis. The logging system should be simple for MVP but extensible for future needs (e.g., filtering, output to files, integration with external tools).
- Integrate a unified event system for communication between subsystems (e.g., input events triggering ECS actions). The event system should be extensible for priorities, propagation (bubbling/capturing), and async support as the engine grows. Document event types and flows.
- Input system should handle backend initialization internally and emit events for integration. Backend can be swapped for future extensibility. Plan for advanced input types (gamepad, touch).
- Plan for robust error handling, especially in resource management, input systems, and event flows. Use exceptions and error reporting consistently. Track resource usage and references for debugging.
- Centralize configuration management and make it extensible for future options (e.g., user profiles, runtime settings). Support live reloading and document configuration usage with templates for common use cases.
- Generalize ResourceManager to support user-defined resource types and hot-reloading for all asset types.
- Expand the renderer with a material/shader system, hierarchical scene graph, and support for multiple rendering backends.
- Expose physics events to ECS and scripting; allow pluggable physics backends.
- Prototype a plugin/extension system for user/community subsystems and tooling.
- Consider in-engine tools (script editor, inspector, debugging UI) to improve developer experience.

## Achieving Maintainability
- Write unit tests for all core logic and interfaces. Maintain high test coverage, especially for integration points.
- Use clear separation of concerns: ECS, Renderer, Physics, Scripting, Resource Manager, Audio.
- Avoid circular dependencies between modules.
- Refactor code regularly to improve readability and structure.
- Maintain up-to-date documentation for code and architecture. Add subsystem diagrams and flowcharts for onboarding.
- Provide example projects and demo scenes to help new users, validate architecture decisions, and demonstrate subsystem interactions via the event system.
- Automate regression and integration tests for demo scenes and edge cases.

## Achieving Flexibility
- Make all subsystems pluggable via interfaces; allow users to swap implementations.
- Support configuration via external files (e.g., JSON, YAML, TOML) for engine settings.
- Use event-driven patterns for extensibility (e.g., ECS event system).
- Allow hot-reloading for scripts and assets where possible.
- Design APIs to be forward-compatible for future features.
- Generalize resource and plugin systems for user/community extension.

## Feature Development
- Start with MVP features; add advanced features incrementally.
- Prototype new features in isolation before integrating into the main codebase.
- Review and discuss architecture decisions before major changes.
- Ensure new features do not break existing functionality or interfaces.
- Gather feedback from early users and iterate on extensibility features.

Follow these rules to ensure simplex-engine remains maintainable, flexible, and easy to extend as it grows.

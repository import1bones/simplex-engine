# Event Types in simplex-engine

- input: Emitted by Input system for each input event (e.g., key press, mouse, custom)
- Custom event types can be registered and emitted via EventSystem

Example:

```python
engine.events.register('input', handler)
engine.events.emit('input', data)
```

See docs/architecture.md for more details on event-driven design.

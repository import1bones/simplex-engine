# Advanced Event System Usage (simplex-engine)

The `EventSystem` supports advanced event handling for extensibility and complex workflows.

## Features
- **Listener Priorities:** Register listeners with a `priority` (higher runs first).
- **Capture/Bubble Phases:** Listeners can run in the capture phase (before bubbling) by setting `capture=True`.
- **Propagation Control:** Listeners can stop event propagation by returning `False`.
- **Extensible:** Add custom event objects, async support, or filtering as needed.

## Example Usage
```python
from simplex.event.event_system import EventSystem

events = EventSystem()

def capture_listener(data):
    print("Capture phase:", data)
    # Returning False stops propagation
    return True

def bubble_listener(data):
    print("Bubble phase:", data)
    return True

events.register('input', capture_listener, priority=10, capture=True)
events.register('input', bubble_listener, priority=5)

events.emit('input', {'key': 'A'})
```


## Extending the EventSystem
- Add async/await support by overriding `emit`.
- Add event filtering or transformation by wrapping listeners.
- Use custom event objects for richer data and propagation control.
- Integrate with plugins or scripting by exposing `register` and `emit`.

## Best Practices
- Use priorities to control event order.
- Use capture for pre-processing or global hooks.
- Always handle exceptions in listeners.
- Return `False` to stop propagation when needed.

---
For more, see the source code in `simplex/event/event_system.py` and in-code docstrings for advanced usage and patterns.

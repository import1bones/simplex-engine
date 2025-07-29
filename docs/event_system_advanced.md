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

## Notes
- Capture listeners run before bubble listeners.
- Listeners with higher priority run first within each phase.
- Returning `False` from any listener stops further propagation.

---
For more, see the source code in `simplex/event/event_system.py`.

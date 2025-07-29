# Event Priorities & Propagation (Bubbling/Capturing)

The EventSystem supports advanced event handling:
- Listener priorities (higher runs first)
- Capture and bubble phases (bubbling/capturing)
- Stopping propagation by returning False

## Usage Example
```python
from simplex.event.event_system import EventSystem

events = EventSystem()

def on_input(data):
    print('Input event:', data)

def on_capture(data):
    print('Capture event:', data)

def stopper(data):
    print('Stopper called')
    return False

events.register('input', on_input, priority=5)
events.register('input', on_capture, priority=10, capture=True)
events.register('input', stopper, priority=1)
events.emit('input', {'key': 'A'})
```

## Notes
- Capture listeners run before bubble listeners.
- Returning False from any listener stops further propagation.
- Priorities control order within each phase.
- See code docstring for more advanced usage.

# Gamepad & Touch Input Support (MVP-3)

The Input system now supports both gamepad and touch input (via pygame FINGER events).

## Features
- Gamepad support (already present): emits `gamepad` events with axes, buttons, hats, and name.
- Touch support: emits `touch` events for FINGERDOWN, FINGERUP, and FINGERMOTION events (with x/y, dx/dy, finger/touch id).
- All other input events are emitted as `input` events.

## Usage Example
```python
from simplex.input.input import Input
from simplex.event.event_system import EventSystem

events = EventSystem()
input_sys = Input(backend="pygame", event_system=events)

def on_touch(event):
    print("Touch event:", event)

def on_gamepad(event):
    print("Gamepad event:", event)

events.register('touch', on_touch)
events.register('gamepad', on_gamepad)

input_sys.poll()  # Call in your main loop
```

## Notes
- Touch events require a touch-capable device and pygame 2.x+.
- Gamepad events require a connected game controller.
- All events are observable and can be extended for custom backends.

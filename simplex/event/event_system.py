"""
Simple event system for simplex-engine MVP.
Allows subsystems to communicate via events.
"""

from typing import Callable, Dict, List, Any
from simplex.utils.logger import log


class EventSystem:
    """
    Advanced Usage:
    - Register listeners with priority (higher runs first):
        events.register('input', listener, priority=10)
    - Register listeners for capture phase (run before bubble):
        events.register('input', capture_listener, capture=True)
    - Stop propagation by returning False from a listener:
        def stop_listener(data):
            ...
            return False
    - Event phases:
        1. Capture: all listeners with capture=True, in priority order
        2. Bubble: all listeners with capture=False, in priority order
    - Extensible for async, filtering, or custom event objects.

    Example:
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
    """

    """
    Basic event system for registering, emitting, and handling events.
    Extensible for priorities, propagation, async support, and advanced features as engine grows.
    Example usage:
        events = EventSystem()
        events.register('input', handler)
        events.emit('input', data)
    """

    def __init__(self):
        # Listeners: event_type -> list of (priority, listener, capture)
        self._listeners: Dict[str, List[tuple]] = {}

    def register(
        self,
        event_type: str,
        listener: Callable[[Any], None],
        priority: int = 0,
        capture: bool = False,
    ) -> None:
        """
        Register a listener for a specific event type.
        Listeners with higher priority are called first. If capture=True, listener is called during capture phase.
        """
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append((priority, listener, capture))
        # Sort listeners by priority (descending)
        self._listeners[event_type].sort(key=lambda x: -x[0])
        log(
            f"Listener registered for event: {event_type} (priority={priority}, capture={capture})",
            level="DEBUG",
        )

    def emit(self, event_type: str, data: Any = None, propagate: bool = True) -> None:
        """
        Emit an event to all registered listeners.
        Supports event priorities and propagation (bubbling/capturing).
        If a listener returns False, propagation is stopped.
        """
        listeners = self._listeners.get(event_type, [])
        log(
            f"Emitting event: {event_type} to {len(listeners)} listeners", level="DEBUG"
        )
        # Capture phase: call listeners with capture=True
        for priority, listener, capture in listeners:
            if capture:
                try:
                    result = listener(data)
                    if result is False and propagate:
                        log(
                            f"Event propagation stopped by capture listener for {event_type}",
                            level="DEBUG",
                        )
                        return
                except Exception as e:
                    log(f"Error in event listener for {event_type}: {e}", level="ERROR")
        # Bubble phase: call listeners with capture=False
        for priority, listener, capture in listeners:
            if not capture:
                try:
                    result = listener(data)
                    if result is False and propagate:
                        log(
                            f"Event propagation stopped by bubble listener for {event_type}",
                            level="DEBUG",
                        )
                        return
                except Exception as e:
                    log(f"Error in event listener for {event_type}: {e}", level="ERROR")

    def shutdown(self) -> None:
        """Clean shutdown of event system."""
        self._listeners.clear()
        log("EventSystem shutdown", level="INFO")

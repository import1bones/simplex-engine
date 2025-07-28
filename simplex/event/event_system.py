"""
Simple event system for simplex-engine MVP.
Allows subsystems to communicate via events.
"""
from typing import Callable, Dict, List, Any
from simplex.utils.logger import log

class EventSystem:
    """
    Basic event system for registering, emitting, and handling events.
    Extensible for priorities, propagation, async support, and advanced features as engine grows.
    Example usage:
        events = EventSystem()
        events.register('input', handler)
        events.emit('input', data)
    """
    def __init__(self):
        self._listeners: Dict[str, List[Callable[[Any], None]]] = {}

    def register(self, event_type: str, listener: Callable[[Any], None]) -> None:
        """Register a listener for a specific event type."""
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(listener)
        log(f"Listener registered for event: {event_type}", level="DEBUG")

    def emit(self, event_type: str, data: Any = None) -> None:
        """Emit an event to all registered listeners."""
        listeners = self._listeners.get(event_type, [])
        log(f"Emitting event: {event_type} to {len(listeners)} listeners", level="DEBUG")
        for listener in listeners:
            try:
                listener(data)
            except Exception as e:
                log(f"Error in event listener for {event_type}: {e}", level="ERROR")

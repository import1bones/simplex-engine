"""
Minimal Input system implementation for MVP.
"""
from .interface import InputInterface
from simplex.utils.logger import log


class Input(InputInterface):
    """
    Input system for simplex-engine MVP.
    Supports flexible backend (e.g., pygame) and error handling.
    Can emit events via an event system.
    """
    def __init__(self, backend=None, event_system=None):
        self.backend = backend
        self.event_system = event_system

    def set_backend(self, backend: str) -> None:
        """
        Set the input backend implementation.
        """
        log(f"Setting input backend: {backend}", level="INFO")
        self.backend = backend

    def poll(self) -> None:
        """
        Poll input events from the backend. Emits events via event system.
        """
        if self.backend == "pygame":
            try:
                import pygame
                pygame.event.pump()
                events = pygame.event.get()
                log(f"Polled {len(events)} pygame events.", level="INFO")
                # Emit events for each pygame event
                if self.event_system:
                    for event in events:
                        self.event_system.emit('input', event)
            except ImportError:
                log("pygame not installed.", level="ERROR")
            except Exception as e:
                log(f"Input polling error: {e}", level="ERROR")
        else:
            log("Polling input events with custom backend...", level="INFO")

    def get_state(self) -> dict:
        """
        Return current input state. Handles errors and logs at INFO level.
        """
        if self.backend == "pygame":
            try:
                import pygame
                keys = pygame.key.get_pressed()
                mouse = pygame.mouse.get_pressed()
                log("Getting pygame input state.", level="INFO")
                return {"keys": keys, "mouse": mouse}
            except ImportError:
                log("pygame not installed.", level="ERROR")
                return {}
            except Exception as e:
                log(f"Input state error: {e}", level="ERROR")
                return {}
        else:
            log("Getting input state with custom backend...", level="INFO")
            return {}

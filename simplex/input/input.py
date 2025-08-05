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
        self._initialized = False

    def _init_pygame(self):
        """
        Initialize pygame and its display if not already done.
        """
        if not self._initialized:
            import pygame
            pygame.init()
            # Create a hidden display to allow event polling
            pygame.display.set_mode((1, 1), pygame.HIDDEN)
            self._initialized = True
    def set_backend(self, backend: str) -> None:
        """
        Set the input backend implementation.
        """
        log(f"Setting input backend: {backend}", level="INFO")
        self.backend = backend

    def poll(self) -> None:
        """
        Poll input events from the backend. Emits events via event system.
        Supports 'pygame' (default) and 'custom' (lightweight placeholder) backends.
        Now supports gamepad and touch input (via pygame FINGER events).
        """
        if self.backend == "pygame":
            try:
                self._init_pygame()
                import pygame
                pygame.event.pump()
                events = pygame.event.get()
                log(f"Polled {len(events)} pygame events.", level="INFO")
                # Emit events for each pygame event
                if self.event_system:
                    for event in events:
                        # Touch support: emit 'touch' for FINGER events
                        if event.type in (getattr(pygame, 'FINGERDOWN', None), getattr(pygame, 'FINGERUP', None), getattr(pygame, 'FINGERMOTION', None)):
                            touch_data = {
                                "type": "touch",
                                "event": event.type,
                                "x": getattr(event, 'x', None),
                                "y": getattr(event, 'y', None),
                                "dx": getattr(event, 'dx', None),
                                "dy": getattr(event, 'dy', None),
                                "finger_id": getattr(event, 'finger_id', None),
                                "touch_id": getattr(event, 'touch_id', None),
                            }
                            self.event_system.emit('touch', touch_data)
                        else:
                            self.event_system.emit('input', event)

                # Gamepad support: detect and emit gamepad events
                pygame.joystick.init()
                num_joysticks = pygame.joystick.get_count()
                for jid in range(num_joysticks):
                    joystick = pygame.joystick.Joystick(jid)
                    joystick.init()
                    gamepad_state = {
                        "id": jid,
                        "name": joystick.get_name(),
                        "axes": [joystick.get_axis(i) for i in range(joystick.get_numaxes())],
                        "buttons": [joystick.get_button(i) for i in range(joystick.get_numbuttons())],
                        "hats": [joystick.get_hat(i) for i in range(joystick.get_numhats())],
                    }
                    log(f"Gamepad detected: {gamepad_state['name']} (id {jid})", level="INFO")
                    if self.event_system:
                        self.event_system.emit('gamepad', gamepad_state)
            except ImportError:
                log("pygame not installed.", level="ERROR")
            except Exception as e:
                log(f"Input polling error: {e}", level="ERROR")
        elif self.backend == "custom":
            # Lightweight backend: just log and emit a fake event for demonstration
            log("Polling input events with custom backend (demo only)...", level="INFO")
            if self.event_system:
                fake_event = {"type": "custom_input", "info": "demo event"}
                self.event_system.emit('input', fake_event)
        else:
            log(f"Unknown input backend: {self.backend}", level="WARNING")

    def get_state(self) -> dict:
        """
        Return current input state. Handles errors and logs at INFO level.
        Extend this method for new backends.
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
        elif self.backend == "custom":
            log("Getting input state with custom backend (demo only)...", level="INFO")
            return {"custom": True}
        else:
            log(f"Unknown input backend: {self.backend}", level="WARNING")
            return {}
    
    def shutdown(self):
        """Clean shutdown of input system."""
        log("Input system shutdown", level="INFO")

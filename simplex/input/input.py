"""
Minimal Input system implementation for MVP.
"""
from .interface import InputInterface
from simplex.utils.logger import log

class Input(InputInterface):
    def __init__(self, backend=None):
        self.backend = backend

    def set_backend(self, backend):
        log(f"Setting input backend: {backend}")
        self.backend = backend

    def poll(self):
        if self.backend == "pygame":
            # Example: poll pygame events
            try:
                import pygame
                pygame.event.pump()
                events = pygame.event.get()
                log(f"Polled {len(events)} pygame events.")
            except ImportError:
                log("pygame not installed.")
        else:
            log("Polling input events with custom backend...")

    def get_state(self):
        if self.backend == "pygame":
            try:
                import pygame
                keys = pygame.key.get_pressed()
                mouse = pygame.mouse.get_pressed()
                log("Getting pygame input state.")
                return {"keys": keys, "mouse": mouse}
            except ImportError:
                log("pygame not installed.")
                return {}
        else:
            log("Getting input state with custom backend...")
            return {}

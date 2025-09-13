"""
Input system interface for simplex-engine.
"""

from abc import ABC, abstractmethod


class InputInterface(ABC):
    """
    Abstract input system interface for simplex-engine.
    Allows flexible backend implementation (e.g., pygame, custom, etc).
    """

    @abstractmethod
    def poll(self):
        """Poll input events from backend."""
        pass

    @abstractmethod
    def get_state(self):
        """Return current input state (keys, mouse, gamepad, etc)."""
        pass

    @abstractmethod
    def set_backend(self, backend):
        """Set the input backend implementation."""
        pass

"""
Audio system interface for simplex-engine.
"""

from abc import ABC, abstractmethod


class AudioInterface(ABC):
    @abstractmethod
    def play(self, sound_id: str):
        pass

    @abstractmethod
    def stop(self, sound_id: str):
        pass

    @abstractmethod
    def load(self, sound_path: str):
        pass

    @abstractmethod
    def unload(self, sound_id: str):
        pass

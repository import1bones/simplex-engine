"""
Minimal Audio system implementation for MVP-2.
"""
from .interface import AudioInterface
from simplex.utils.logger import log

class Audio(AudioInterface):
    """
    Audio system for simplex-engine MVP-2.
    Handles audio playback, stop, and resource management.
    """
    def __init__(self, resource_manager=None):
        self.sounds = {}
        self.resource_manager = resource_manager
        try:
            import pygame
            pygame.mixer.init()
            self._mixer = pygame.mixer
        except ImportError:
            log("pygame not installed. Audio will not work.", level="ERROR")
            self._mixer = None
        except Exception as e:
            log(f"Audio system init error: {e}", level="ERROR")
            self._mixer = None

    def load(self, sound_path: str):
        if not self._mixer:
            return
        # Use resource manager to load the sound if available
        if self.resource_manager:
            self.resource_manager.load(sound_path)
        try:
            sound = self._mixer.Sound(sound_path)
            self.sounds[sound_path] = sound
            log(f"Loaded sound: {sound_path}", level="INFO")
        except Exception as e:
            log(f"Audio load error: {e}", level="ERROR")

    def unload(self, sound_id: str):
        if sound_id in self.sounds:
            del self.sounds[sound_id]
            log(f"Unloaded sound: {sound_id}", level="INFO")
        if self.resource_manager:
            self.resource_manager.unload(sound_id)

    def play(self, sound_id: str):
        sound = self.sounds.get(sound_id)
        if sound:
            try:
                sound.play()
                log(f"Playing sound: {sound_id}", level="INFO")
            except Exception as e:
                log(f"Audio play error: {e}", level="ERROR")
        else:
            log(f"Sound not loaded: {sound_id}", level="WARNING")

    def stop(self, sound_id: str):
        sound = self.sounds.get(sound_id)
        if sound:
            try:
                sound.stop()
                log(f"Stopped sound: {sound_id}", level="INFO")
            except Exception as e:
                log(f"Audio stop error: {e}", level="ERROR")
        else:
            log(f"Sound not loaded: {sound_id}", level="WARNING")

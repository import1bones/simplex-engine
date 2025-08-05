"""
Minimal Audio system implementation for MVP-2 with proper dependency injection.
"""
from .interface import AudioInterface
from simplex.utils.logger import log

class Audio(AudioInterface):
    """
    Audio system for simplex-engine with event system integration.
    Handles audio playback, stop, and resource management.
    """
    def __init__(self, event_system=None, resource_manager=None):
        self.event_system = event_system
        self.resource_manager = resource_manager
        self.sounds = {}
        self._mixer = None
        self._initialized = False
        
        self._initialize_audio_backend()
        log("Audio system created", level="INFO")
    
    def _initialize_audio_backend(self):
        """Initialize audio backend (pygame mixer)."""
        try:
            import pygame
            pygame.mixer.init()
            self._mixer = pygame.mixer
            self._initialized = True
            log("Audio backend initialized with pygame", level="INFO")
        except ImportError:
            log("pygame not installed. Audio will not work.", level="WARNING")
            self._mixer = None
        except Exception as e:
            log(f"Audio system init error: {e}", level="ERROR")
            self._mixer = None
    
    def update(self, delta_time):
        """Update audio system - called every frame."""
        # Could be used for music fading, 3D audio positioning, etc.
        pass

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
        if not self._initialized:
            log("Audio not initialized, cannot play sound", level="WARNING")
            return
            
        sound = self.sounds.get(sound_id)
        if sound:
            try:
                sound.play()
                log(f"Playing sound: {sound_id}", level="INFO")
                if self.event_system:
                    self.event_system.emit('audio_play', {'sound_id': sound_id})
            except Exception as e:
                log(f"Audio play error: {e}", level="ERROR")
        else:
            log(f"Sound not loaded: {sound_id}", level="WARNING")

    def stop(self, sound_id: str):
        if not self._initialized:
            log("Audio not initialized, cannot stop sound", level="WARNING")
            return
            
        sound = self.sounds.get(sound_id)
        if sound:
            try:
                sound.stop()
                log(f"Stopped sound: {sound_id}", level="INFO")
                if self.event_system:
                    self.event_system.emit('audio_stop', {'sound_id': sound_id})
            except Exception as e:
                log(f"Audio stop error: {e}", level="ERROR")
        else:
            log(f"Sound not loaded: {sound_id}", level="WARNING")
    
    def shutdown(self):
        """Clean shutdown of audio system."""
        if self._mixer:
            try:
                self._mixer.quit()
            except:
                pass
        
        self.sounds.clear()
        self._initialized = False
        log("Audio system shutdown", level="INFO")

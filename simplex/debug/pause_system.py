"""
Engine pause/resume system for debugging and development.
"""

from typing import Dict, Any
from enum import Enum


class EngineState(Enum):
    """Engine execution states."""

    RUNNING = "running"
    PAUSED = "paused"
    STEPPING = "stepping"  # Single frame step mode


class PauseSystem:
    """Manages engine pause/resume functionality."""

    def __init__(self):
        self.state = EngineState.RUNNING
        self.step_requested = False
        self.pause_callbacks = []
        self.resume_callbacks = []

    def pause(self):
        """Pause the engine."""
        if self.state == EngineState.RUNNING:
            self.state = EngineState.PAUSED
            self._trigger_pause_callbacks()

    def resume(self):
        """Resume the engine."""
        if self.state in [EngineState.PAUSED, EngineState.STEPPING]:
            self.state = EngineState.RUNNING
            self._trigger_resume_callbacks()

    def toggle_pause(self):
        """Toggle between paused and running states."""
        if self.state == EngineState.RUNNING:
            self.pause()
        else:
            self.resume()

    def step_frame(self):
        """Request a single frame step while paused."""
        if self.state == EngineState.PAUSED:
            self.state = EngineState.STEPPING
            self.step_requested = True

    def is_paused(self) -> bool:
        """Check if engine is paused."""
        return self.state in [EngineState.PAUSED, EngineState.STEPPING]

    def is_running(self) -> bool:
        """Check if engine is running normally."""
        return self.state == EngineState.RUNNING

    def should_update(self) -> bool:
        """Check if systems should update this frame."""
        if self.state == EngineState.RUNNING:
            return True
        elif self.state == EngineState.STEPPING and self.step_requested:
            self.step_requested = False
            self.state = EngineState.PAUSED  # Return to paused after step
            return True
        return False

    def get_state_info(self) -> Dict[str, Any]:
        """Get current state information."""
        return {
            "state": self.state.value,
            "paused": self.is_paused(),
            "can_step": self.state == EngineState.PAUSED,
        }

    def add_pause_callback(self, callback):
        """Add callback to execute when engine is paused."""
        self.pause_callbacks.append(callback)

    def add_resume_callback(self, callback):
        """Add callback to execute when engine is resumed."""
        self.resume_callbacks.append(callback)

    def _trigger_pause_callbacks(self):
        """Trigger all pause callbacks."""
        for callback in self.pause_callbacks:
            try:
                callback()
            except Exception as e:
                print(f"Error in pause callback: {e}")

    def _trigger_resume_callbacks(self):
        """Trigger all resume callbacks."""
        for callback in self.resume_callbacks:
            try:
                callback()
            except Exception as e:
                print(f"Error in resume callback: {e}")


class DevToolsManager:
    """Central manager for development tools."""

    def __init__(self):
        self.pause_system = PauseSystem()
        self.debug_enabled = True
        self.profiling_enabled = False
        self.frame_by_frame_mode = False

    def handle_debug_input(self, key) -> bool:
        """Handle debug-related input. Returns True if input was consumed."""
        if key == "F1":
            self.toggle_debug()
            return True
        elif key == "F2":
            self.pause_system.toggle_pause()
            return True
        elif key == "F3":
            self.pause_system.step_frame()
            return True
        elif key == "F4":
            self.toggle_profiling()
            return True
        return False

    def toggle_debug(self):
        """Toggle debug overlay."""
        self.debug_enabled = not self.debug_enabled

    def toggle_profiling(self):
        """Toggle performance profiling."""
        self.profiling_enabled = not self.profiling_enabled

    def get_dev_stats(self) -> Dict[str, Any]:
        """Get development tool statistics."""
        stats = {
            "Debug": "ON" if self.debug_enabled else "OFF",
            "Profiling": "ON" if self.profiling_enabled else "OFF",
        }
        stats.update(self.pause_system.get_state_info())
        return stats

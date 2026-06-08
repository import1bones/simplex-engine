"""
ScriptEditorInterface for simplex-engine.
Defines the interface for in-engine script editors (CLI or GUI).
"""

from abc import ABC, abstractmethod


class ScriptEditorInterface(ABC):
    @abstractmethod
    def list_scripts(self):
        """List available scripts for editing."""
        pass

    @abstractmethod
    def view_script(self, script_path):
        """Display the contents of a script."""
        pass

    @abstractmethod
    def edit_script(self, script_path):
        """Edit a script (implementation may vary: CLI, GUI, etc.)."""
        pass

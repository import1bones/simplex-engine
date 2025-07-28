"""
Minimal ScriptManager implementation for MVP.
"""

from .interface import ScriptManagerInterface
from simplex.utils.logger import log

class ScriptManager(ScriptManagerInterface):
    """
    Script manager for simplex-engine MVP.
    Handles script execution and error management.
    """
    def execute(self) -> None:
        """
        Execute scripts. Logs at INFO level and handles errors.
        """
        try:
            log("Executing scripts...", level="INFO")
            # Future: actual script execution logic
        except Exception as e:
            log(f"Script execution error: {e}", level="ERROR")

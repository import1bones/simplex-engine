"""
Example plugin for ScriptManager MVP-3.
This plugin logs when a script is loaded or reloaded.
"""
from simplex.utils.logger import log

def script_event_logger(script_path, module):
    log(f"[PLUGIN] Script event: {script_path} loaded/reloaded.", level="INFO")
    log(f"[PLUGIN] Script event: hello world!")
# Usage in engine setup:
# from simplex.script.script_manager import ScriptManager
# mgr = ScriptManager()
# mgr.on("on_load", script_event_logger)
# mgr.on("on_reload", script_event_logger)
# mgr.hot_reload()  # or mgr.execute()

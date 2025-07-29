"""
Minimal ScriptManager implementation for MVP.
"""

from .interface import ScriptManagerInterface
from simplex.utils.logger import log

class ScriptManager(ScriptManagerInterface):
    import traceback

    def __init__(self, script_dir: str = "examples/mvp/scripts"):
        self.script_dir = script_dir
        self._script_mtimes = {}
        self._plugins = []
        # Event hooks: on_load, on_reload, on_error
        self._event_hooks = {"on_load": [], "on_reload": [], "on_error": []}
        self._recent_errors = []  # Store recent script errors for debugging
    import os
    import importlib.util
    import time

    def __init__(self, script_dir: str = "examples/mvp/scripts"):
        self.script_dir = script_dir
        self._script_mtimes = {}
        self._plugins = []
        # Event hooks: on_load, on_reload, on_error
        self._event_hooks = {"on_load": [], "on_reload": [], "on_error": []}

    def register_plugin(self, plugin_func):
        """Register a plugin callback to be called after script execution."""
        self._plugins.append(plugin_func)

    def on(self, event, callback):
        """Register an event hook: on_load, on_reload, on_error."""
        if event in self._event_hooks:
            self._event_hooks[event].append(callback)

    def _emit(self, event, *args, **kwargs):
        for cb in self._event_hooks.get(event, []):
            try:
                cb(*args, **kwargs)
            except Exception as e:
                log(f"Event hook error: {e}", level="ERROR")

    def discover_scripts(self):
        """Return a list of .py script file paths in the script directory."""
        try:
            return [self.os.path.join(self.script_dir, f)
                    for f in self.os.listdir(self.script_dir)
                    if f.endswith('.py')]
        except Exception as e:
            tb = self.traceback.format_exc()
            log(f"Script discovery error: {e}\n{tb}", level="ERROR")
            self._recent_errors.append(("discovery", None, tb))
            return []

    def hot_reload(self):
        """Hot-reload and execute all scripts if changed."""
        for script_path in self.discover_scripts():
            try:
                mtime = self.os.path.getmtime(script_path)
                last_mtime = self._script_mtimes.get(script_path, 0)
                if mtime > last_mtime:
                    self._script_mtimes[script_path] = mtime
                    spec = self.importlib.util.spec_from_file_location(self.os.path.basename(script_path)[:-3], script_path)
                    module = self.importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    if hasattr(module, "run"):
                        module.run()
                    for plugin in self._plugins:
                        try:
                            plugin(module)
                        except Exception as e:
                            tb = self.traceback.format_exc()
                            log(f"Plugin error: {e}\n{tb}", level="ERROR")
                            self._recent_errors.append(("plugin", script_path, tb))
                    event_type = "on_reload" if last_mtime > 0 else "on_load"
                    self._emit(event_type, script_path, module)
                    log(f"Hot-reloaded and executed: {script_path}", level="INFO")
            except Exception as e:
                tb = self.traceback.format_exc()
                self._emit("on_error", script_path, e)
                log(f"Hot-reload error in {script_path}: {e}\n{tb}", level="ERROR")
                self._recent_errors.append(("hot_reload", script_path, tb))
    """
    Script manager for simplex-engine MVP.
    Handles script execution and error management.
    """
    def execute(self) -> None:
        """
        Execute all scripts in the script directory (once, not hot-reload).
        """
        for script_path in self.discover_scripts():
            try:
                spec = self.importlib.util.spec_from_file_location(self.os.path.basename(script_path)[:-3], script_path)
                module = self.importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                if hasattr(module, "run"):
                    module.run()
                for plugin in self._plugins:
                    try:
                        plugin(module)
                    except Exception as e:
                        tb = self.traceback.format_exc()
                        log(f"Plugin error: {e}\n{tb}", level="ERROR")
                        self._recent_errors.append(("plugin", script_path, tb))
                self._emit("on_load", script_path, module)
                log(f"Executed: {script_path}", level="INFO")
            except Exception as e:
                tb = self.traceback.format_exc()
                self._emit("on_error", script_path, e)
                log(f"Script execution error in {script_path}: {e}\n{tb}", level="ERROR")
                self._recent_errors.append(("execute", script_path, tb))

    def get_recent_errors(self, limit=10):
        """Return a list of recent script errors for debugging."""
        return self._recent_errors[-limit:]

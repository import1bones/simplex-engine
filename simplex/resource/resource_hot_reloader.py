"""
ResourceHotReloader for simplex-engine MVP-3.
Watches resource files and triggers reloads on change.
"""
import os
import time
from simplex.utils.logger import log

class ResourceHotReloader:
    def __init__(self, resource_manager, watch_paths, poll_interval=1.0):
        self.resource_manager = resource_manager
        self.watch_paths = watch_paths  # List of file paths to watch
        self.poll_interval = poll_interval
        self._mtimes = {}
        self._running = False
        self._event_hooks = {"on_reload": [], "on_error": []}

    def on(self, event, callback):
        if event in self._event_hooks:
            self._event_hooks[event].append(callback)

    def _emit(self, event, *args, **kwargs):
        for cb in self._event_hooks.get(event, []):
            try:
                cb(*args, **kwargs)
            except Exception as e:
                log(f"ResourceHotReloader event error: {e}", level="ERROR")

    def poll(self):
        """Poll watched files for changes and reload if needed."""
        for path in self.watch_paths:
            try:
                mtime = os.path.getmtime(path)
                last_mtime = self._mtimes.get(path, 0)
                if mtime > last_mtime:
                    self._mtimes[path] = mtime
                    self.resource_manager.reload(path)
                    self._emit("on_reload", path)
                    log(f"Hot-reloaded resource: {path}", level="INFO")
            except Exception as e:
                self._emit("on_error", path, e)
                log(f"Resource hot-reload error for {path}: {e}", level="ERROR")

    def run_once(self):
        self.poll()

    def run_forever(self):
        self._running = True
        while self._running:
            self.poll()
            time.sleep(self.poll_interval)

    def stop(self):
        self._running = False

"""
ConfigHotReloader for simplex-engine MVP-3.
Watches the config file and reloads it on change, emitting an event.
"""

import os
import time
from simplex.utils.logger import log


class ConfigHotReloader:
    def __init__(self, config, config_path, event_system=None, poll_interval=1.0):
        self.config = config
        self.config_path = config_path
        self.event_system = event_system
        self.poll_interval = poll_interval
        self._last_mtime = 0
        self._running = False

    def poll(self):
        try:
            mtime = os.path.getmtime(self.config_path)
            if mtime > self._last_mtime:
                self._last_mtime = mtime
                self.config.reload()  # Assumes Config has a reload() method
                log(f"Config hot-reloaded: {self.config_path}", level="INFO")
                if self.event_system:
                    self.event_system.emit("config_reload", self.config)
        except Exception as e:
            log(f"Config hot-reload error: {e}", level="ERROR")

    def run_once(self):
        self.poll()

    def run_forever(self):
        self._running = True
        while self._running:
            self.poll()
            time.sleep(self.poll_interval)

    def stop(self):
        self._running = False

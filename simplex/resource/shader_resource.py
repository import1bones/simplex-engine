from .interface import ResourceManagerInterface


import os
import time
from simplex.utils.logger import log


class ShaderResource:
    """Shader resource, managed and hot-reloadable by ResourceManager."""

    def __init__(self, path: str):
        self.path = path
        self.source = None
        self.last_modified = None

    def load(self):
        """Load shader source from file and track last modification time."""
        if not os.path.isfile(self.path):
            log(f"Shader file not found: {self.path}", level="ERROR")
            raise FileNotFoundError(f"Shader file not found: {self.path}")
        with open(self.path, "r") as f:
            self.source = f.read()
        self.last_modified = os.path.getmtime(self.path)
        log(f"Shader loaded: {self.path}", level="INFO")

    def reload(self):
        """Reload shader source if file has changed since last load."""
        if not os.path.isfile(self.path):
            log(f"Shader file not found: {self.path}", level="ERROR")
            raise FileNotFoundError(f"Shader file not found: {self.path}")
        current_mtime = os.path.getmtime(self.path)
        if self.last_modified is None or current_mtime > self.last_modified:
            with open(self.path, "r") as f:
                self.source = f.read()
            self.last_modified = current_mtime
            log(f"Shader reloaded: {self.path}", level="INFO")
        else:
            log(f"Shader not changed: {self.path}", level="DEBUG")

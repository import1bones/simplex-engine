"""
Simple configuration loader for engine settings.
"""
import toml

class Config:
    def __init__(self, path: str):
        self.path = path
        self.data = toml.load(path)

    def reload(self):
        self.data = toml.load(self.path)

    def get(self, key, default=None):
        return self.data.get(key, default)

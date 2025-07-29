from .interface import ResourceManagerInterface

class ShaderResource:
    """Stub for a shader resource, to be managed and hot-reloaded by ResourceManager."""
    def __init__(self, path: str):
        self.path = path
        self.source = None
        self.last_modified = None

    def load(self):
        # TODO: Load shader source from file
        pass

    def reload(self):
        # TODO: Reload shader source if file changed
        pass

from abc import ABC, abstractmethod


class HotReloadable(ABC):
    """Interface for resources that support hot-reloading."""

    @abstractmethod
    def reload(self):
        pass

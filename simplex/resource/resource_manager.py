"""
Minimal ResourceManager implementation for MVP.
"""

from .interface import ResourceManagerInterface
from simplex.utils.logger import log

    def load(self, resource_path: str):
        log(f"Loading resource: {resource_path}")

    def unload(self, resource_path: str):
        log(f"Unloading resource: {resource_path}")

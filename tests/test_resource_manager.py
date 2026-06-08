import unittest
from simplex.resource.resource_manager import ResourceManager


class TestResourceManager(unittest.TestCase):
    def test_load_and_unload(self):
        rm = ResourceManager()
        rm.load("test_resource")
        self.assertIn("test_resource", rm._cache)
        rm.unload("test_resource")
        self.assertNotIn("test_resource", rm._cache)


if __name__ == "__main__":
    unittest.main()

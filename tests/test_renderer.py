import unittest
from simplex.renderer.renderer import Renderer

class TestRenderer(unittest.TestCase):
    def test_add_primitive(self):
        renderer = Renderer()
        node = renderer.add_primitive('cube', material='mat1')
        self.assertEqual(node.primitive, 'cube')
        self.assertEqual(node.material, 'mat1')

if __name__ == '__main__':
    unittest.main()

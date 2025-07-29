
import unittest
from simplex.renderer.renderer import Renderer
from simplex.renderer.material import Material

class TestRenderer(unittest.TestCase):
    def test_add_primitive(self):
        renderer = Renderer()
        # Create and register a Material object
        mat = Material('mat1', properties={'color': (1, 1, 1)})
        renderer.register_material(mat)
        node = renderer.add_primitive('cube', material='mat1')
        self.assertEqual(node.primitive, 'cube')
        self.assertEqual(node.material.name, 'mat1')

if __name__ == '__main__':
    unittest.main()

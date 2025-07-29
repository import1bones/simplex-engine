import unittest
from simplex.input.input import Input

class TestInput(unittest.TestCase):
    def test_custom_backend(self):
        input_sys = Input(backend='custom')
        input_sys.poll()  # Should log and emit a fake event
        state = input_sys.get_state()
        self.assertTrue(state.get('custom'))

if __name__ == '__main__':
    unittest.main()

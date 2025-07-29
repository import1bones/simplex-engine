import unittest
from simplex.script.script_manager import ScriptManager

class TestScriptManager(unittest.TestCase):
    def test_execute(self):
        sm = ScriptManager()
        sm.execute()  # Should log execution
    def test_hot_reload(self):
        sm = ScriptManager()
        sm.hot_reload()  # Should log hot-reload (no-op if file not found)

if __name__ == '__main__':
    unittest.main()

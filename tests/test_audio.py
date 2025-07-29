import unittest
from simplex.audio.audio import Audio

class DummyResourceManager:
    def load(self, path):
        self.loaded = path
    def unload(self, path):
        self.unloaded = path

class TestAudio(unittest.TestCase):
    def test_load_and_play(self):
        audio = Audio(resource_manager=DummyResourceManager())
        # This will not actually play sound, but will test logic paths
        audio.load('test.wav')
        self.assertIn('test.wav', audio.sounds)
        audio.play('test.wav')
        audio.stop('test.wav')
        audio.unload('test.wav')
        self.assertNotIn('test.wav', audio.sounds)

if __name__ == '__main__':
    unittest.main()

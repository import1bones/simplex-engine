
import unittest
from unittest.mock import patch, MagicMock
from simplex.audio.audio import Audio

class DummyResourceManager:
    def load(self, path):
        self.loaded = path
    def unload(self, path):
        self.unloaded = path

class TestAudio(unittest.TestCase):
    @patch('pygame.mixer.Sound')
    @patch('pygame.mixer.init')
    def test_load_and_play(self, mock_init, mock_sound):
        mock_sound.return_value = MagicMock(play=MagicMock(), stop=MagicMock())
        audio = Audio(resource_manager=DummyResourceManager())
        audio.load('test.wav')
        self.assertIn('test.wav', audio.sounds)
        audio.play('test.wav')
        audio.stop('test.wav')
        audio.unload('test.wav')
        self.assertNotIn('test.wav', audio.sounds)

if __name__ == '__main__':
    unittest.main()

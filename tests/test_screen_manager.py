import unittest
from unittest.mock import Mock

from epub_editor_pro.screens.screen_manager import ScreenManager


class TestScreenManager(unittest.TestCase):

    def setUp(self):
        """Set up for the tests."""
        self.mock_app = Mock()
        self.screen_manager = ScreenManager(self.mock_app)

    def test_push_screen(self):
        """Test that push calls the app's push_screen method."""
        self.screen_manager.push("test_screen")
        self.mock_app.push_screen.assert_called_once_with("test_screen")

    def test_pop_screen(self):
        """Test that pop calls the app's pop_screen method."""
        self.screen_manager.pop()
        self.mock_app.pop_screen.assert_called_once()

    def test_switch_to_screen(self):
        """Test that switch_to calls the app's switch_screen method."""
        self.screen_manager.switch_to("test_screen")
        self.mock_app.switch_screen.assert_called_once_with("test_screen")


if __name__ == "__main__":
    unittest.main()

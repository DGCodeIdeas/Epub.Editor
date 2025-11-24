import json
import unittest
from pathlib import Path
from unittest.mock import patch, mock_open

from epub_editor_pro.core.settings_model import Settings, SettingsManager


class TestSettingsModel(unittest.TestCase):

    def setUp(self):
        """Set up for the tests."""
        self.defaults = {
            "theme": "dark",
            "autosave": True,
            "show_line_numbers": True,
        }
        self.user_settings = {
            "theme": "light",
            "autosave": False,
        }
        self.default_path = Path("defaults.json")
        self.user_path = Path("user.json")

    @patch("pathlib.Path.exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_load_settings_merges_correctly(self, mock_file, mock_exists):
        """Test that settings are merged correctly."""
        mock_exists.side_effect = [True, True]  # default settings, user settings
        mock_file.side_effect = [
            mock_open(read_data=json.dumps(self.defaults)).return_value,
            mock_open(read_data=json.dumps(self.user_settings)).return_value,
        ]

        manager = SettingsManager(self.default_path, self.user_path)

        self.assertEqual(manager.settings.theme, "light")
        self.assertEqual(manager.settings.autosave, False)
        self.assertEqual(manager.settings.show_line_numbers, True)

    @patch("pathlib.Path.exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_load_settings_handles_missing_user_file(self, mock_file, mock_exists):
        """Test that loading works with a missing user file."""
        mock_exists.side_effect = [True, False]  # default settings, user settings
        mock_file.return_value = mock_open(read_data=json.dumps(self.defaults)).return_value

        manager = SettingsManager(self.default_path, self.user_path)

        self.assertEqual(manager.settings.theme, "dark")
        self.assertEqual(manager.settings.autosave, True)

    @patch("pathlib.Path.exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_load_settings_handles_invalid_json(self, mock_file, mock_exists):
        """Test that loading handles invalid JSON."""
        mock_exists.return_value = True
        mock_file.side_effect = [
            mock_open(read_data=json.dumps(self.defaults)).return_value,
            mock_open(read_data="invalid json").return_value,
        ]

        manager = SettingsManager(self.default_path, self.user_path)

        self.assertEqual(manager.settings.theme, "dark")
        self.assertEqual(manager.settings.autosave, True)

    @patch("pathlib.Path.parent")
    @patch("builtins.open", new_callable=mock_open)
    def test_save_settings(self, mock_file, mock_parent):
        """Test that settings are saved correctly."""
        mock_parent.mkdir.return_value = None
        manager = SettingsManager(self.default_path, self.user_path)
        manager.settings.theme = "custom"
        manager.save_settings()

        mock_file.assert_called_once_with(self.user_path, "w")
        handle = mock_file()

        saved_data = "".join(call.args[0] for call in handle.write.call_args_list)
        saved_settings = json.loads(saved_data)

        self.assertEqual(saved_settings["theme"], "custom")

    def test_get_and_set_methods(self):
        """Test the get and set methods."""
        manager = SettingsManager(Path("dummy"), Path("dummy"))
        manager.set("theme", "solarized")
        self.assertEqual(manager.get("theme"), "solarized")

        manager.set("non_existent", True)
        self.assertIsNone(manager.get("non_existent"))


if __name__ == "__main__":
    unittest.main()

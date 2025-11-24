import json
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Dict, Any

@dataclass
class Settings:
    """Represents the application settings."""
    theme: str = "dark"
    autosave: bool = True
    show_line_numbers: bool = True

    def to_dict(self) -> Dict[str, Any]:
        """Converts the settings to a dictionary."""
        return asdict(self)

class SettingsManager:
    """Manages loading, merging, and saving settings."""

    def __init__(self, default_settings_path: Path, user_settings_path: Path):
        self.default_settings_path = default_settings_path
        self.user_settings_path = user_settings_path
        self.settings = self._load_settings()

    def _load_settings(self) -> Settings:
        """Loads settings from default and user files, merging them."""
        defaults = self._load_json_file(self.default_settings_path)
        user_settings = self._load_json_file(self.user_settings_path)

        merged_settings = {**defaults, **user_settings}
        return Settings(**merged_settings)

    def _load_json_file(self, path: Path) -> Dict[str, Any]:
        """Loads a JSON file, returning an empty dict if it doesn't exist."""
        if not path.exists():
            return {}
        try:
            with open(path, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            # Log this error in a real application
            return {}

    def save_settings(self):
        """Saves the current settings to the user settings file."""
        try:
            self.user_settings_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.user_settings_path, "w") as f:
                json.dump(self.settings.to_dict(), f, indent=2)
        except IOError:
            # Log this error in a real application
            pass

    def get(self, key: str, default: Any = None) -> Any:
        """Gets a setting value by key."""
        return getattr(self.settings, key, default)

    def set(self, key: str, value: Any):
        """Sets a setting value by key."""
        if hasattr(self.settings, key):
            setattr(self.settings, key, value)

    def __getattr__(self, name: str) -> Any:
        """Allows direct access to settings attributes."""
        if hasattr(self.settings, name):
            return getattr(self.settings, name)
        raise AttributeError(f"'SettingsManager' object has no attribute '{name}'")

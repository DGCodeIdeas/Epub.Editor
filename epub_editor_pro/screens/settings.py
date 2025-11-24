from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Switch
from textual.containers import VerticalScroll, Vertical
from textual.binding import Binding

from epub_editor_pro.ui.material_components import Card


class SettingsScreen(Screen):
    """A screen for configuring application settings."""

    BINDINGS = [
        Binding("escape", "pop_screen", "Back"),
    ]

    def action_pop_screen(self) -> None:
        """Pop the screen from the navigation stack."""
        self.app.screen_manager.pop()

    def compose(self) -> ComposeResult:
        """Create child widgets for the screen."""
        yield Header()
        with VerticalScroll(id="settings-body"):
            yield self.make_appearance_card()
            yield self.make_behavior_card()
            yield Card(
                "Keybindings",
                Static("Keybinding customization is not yet available."),
                id="keybindings-card",
            )
        yield Footer()

    def make_appearance_card(self) -> Card:
        """Create the appearance settings card."""
        settings_manager = self.app.settings_manager
        return Card(
            "Appearance",
            Vertical(
                Static("Dark Mode"),
                Switch(
                    value=settings_manager.get("theme") == "dark", id="dark_mode"
                ),
            ),
            Vertical(
                Static("Show Line Numbers"),
                Switch(
                    value=settings_manager.get("show_line_numbers", True),
                    id="show_line_numbers",
                ),
            ),
            id="appearance-card",
        )

    def make_behavior_card(self) -> Card:
        """Create the behavior settings card."""
        settings_manager = self.app.settings_manager
        return Card(
            "Behavior",
            Vertical(
                Static("Autosave"),
                Switch(value=settings_manager.get("autosave", True), id="autosave"),
            ),
            id="behavior-card",
        )

    def on_switch_changed(self, event: Switch.Changed) -> None:
        """Handle switch changes and save settings."""
        settings_manager = self.app.settings_manager
        setting_key = str(event.switch.id)

        if setting_key == "dark_mode":
            self.app.action_toggle_dark()
        else:
            settings_manager.set(setting_key, event.value)
            self.app.notify(f"{setting_key.replace('_', ' ').title()} set to {event.value}")
            settings_manager.save_settings()

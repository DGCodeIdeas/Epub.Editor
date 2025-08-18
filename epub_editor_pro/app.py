from pathlib import Path
from textual.app import App, ComposeResult
from textual.widgets import Label
from textual.screen import Screen

from epub_editor_pro.core.epub_model import EpubBook
from epub_editor_pro.screens.file_manager import FileManager
from epub_editor_pro.screens.dashboard import Dashboard

class EpsilonApp(App):
    """A Textual app to edit EPUBs."""

    SCREENS = {
        "file_manager": FileManager,
        "dashboard": Dashboard,
    }

    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("q", "quit", "Quit"),
    ]

    def __init__(self):
        super().__init__()
        self.book: EpubBook | None = None

    def on_mount(self) -> None:
        """Called when the app is first mounted."""
        self.push_screen("file_manager")

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

    def on_file_manager_file_selected(self, event: FileManager.FileSelected) -> None:
        """Handle file selection from the FileManager."""
        from epub_editor_pro.core.epub_loader import EpubLoader, InvalidEpubFileError
        try:
            loader = EpubLoader(event.path)
            self.book = loader.load()
            self.push_screen("dashboard")
        except InvalidEpubFileError as e:
            self.notify(f"Error loading EPUB: {e}", title="Error", severity="error")
        except Exception as e:
            self.notify(f"An unexpected error occurred: {e}", title="Error", severity="error")


def main():
    """Run the application."""
    app = EpsilonApp()
    app.run()

if __name__ == "__main__":
    main()

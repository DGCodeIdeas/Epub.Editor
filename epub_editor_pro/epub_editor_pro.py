from pathlib import Path
from textual.app import App

from epub_editor_pro.core.epub_model import EpubBook
from epub_editor_pro.core.settings_model import SettingsManager
from epub_editor_pro.screens.screen_manager import ScreenManager
from epub_editor_pro.screens.file_manager import FileManager
from epub_editor_pro.screens.dashboard import Dashboard
from epub_editor_pro.screens.search import SearchScreen
from epub_editor_pro.screens.search_results import SearchResultsScreen
from epub_editor_pro.screens.replace import ReplaceScreen
from epub_editor_pro.screens.settings import SettingsScreen
from epub_editor_pro.screens.batch_operations import BatchOperationsScreen
from epub_editor_pro.screens.help import HelpScreen
from epub_editor_pro.core.search_engine import SearchEngine
from epub_editor_pro.core.replace_engine import ReplaceEngine
from epub_editor_pro.core.epub_saver import EpubSaver


DEFAULT_SETTINGS_PATH = Path("config/defaults.json")
USER_SETTINGS_PATH = Path("config/app_config.json")


class EpsilonApp(App):
    """A Textual app to edit EPUBs."""

    SCREENS = {
        "file_manager": FileManager,
        "dashboard": Dashboard,
        "search": SearchScreen,
        "search_results": SearchResultsScreen,
        "replace": ReplaceScreen,
        "settings": SettingsScreen,
        "batch_operations": BatchOperationsScreen,
        "help": HelpScreen,
    }

    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("q", "quit", "Quit"),
        ("f1", "show_help", "Help"),
    ]

    def __init__(self):
        super().__init__()
        self.settings_manager = SettingsManager(
            default_settings_path=DEFAULT_SETTINGS_PATH,
            user_settings_path=USER_SETTINGS_PATH,
        )
        self.screen_manager = ScreenManager(self)
        self.book: EpubBook | None = None
        self.search_results = []

    def action_show_help(self) -> None:
        """Show the help screen."""
        self.screen_manager.push("help")

    def on_mount(self) -> None:
        """Called when the app is first mounted."""
        self.dark = self.settings_manager.get("theme") == "dark"
        self.screen_manager.push("file_manager")

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark
        self.settings_manager.set("theme", "dark" if self.dark else "light")
        self.settings_manager.save_settings()
        self.notify(f"Theme set to {'dark' if self.dark else 'light'}")

    def on_file_manager_file_selected(self, event: FileManager.FileSelected) -> None:
        """Handle file selection from the FileManager."""
        from epub_editor_pro.core.epub_loader import EpubLoader, InvalidEpubFileError
        try:
            loader = EpubLoader(event.path)
            self.book = loader.load()
            self.screen_manager.push("dashboard")
        except InvalidEpubFileError as e:
            self.notify(f"Error loading EPUB: {e}", title="Error", severity="error")
        except Exception as e:
            self.notify(f"An unexpected error occurred: {e}", title="Error", severity="error")

    def on_search_screen_search_initiated(self, event: SearchScreen.SearchInitiated) -> None:
        """Handle search initiation from the SearchScreen."""
        if not self.book:
            self.notify("No EPUB loaded.", title="Error", severity="error")
            return

        try:
            search_engine = SearchEngine(self.book)
            self.search_results = list(search_engine.search(
                event.query,
                event.case_sensitive,
                event.whole_word,
                event.regex
            ))
            self.notify(f"Found {len(self.search_results)} results.", title="Search Complete")
            if self.search_results:
                self.screen_manager.push("search_results")
            else:
                self.screen_manager.pop()  # Go back to dashboard if no results
        except ValueError as e:
            self.notify(str(e), title="Search Error", severity="error")
        except Exception as e:
            self.notify(
                f"An unexpected error occurred during search: {e}",
                title="Error",
                severity="error",
            )

    def on_search_results_screen_replace_selection(
        self, event: SearchResultsScreen.ReplaceSelection
    ) -> None:
        """Handle the selection of a search result for replacement."""
        self.screen_manager.push(ReplaceScreen(search_result=event.search_result))

    def on_replace_screen_replace_initiated(self, event: ReplaceScreen.ReplaceInitiated) -> None:
        """Handle replace initiation from the ReplaceScreen."""
        if not self.book:
            self.notify("No EPUB loaded.", title="Error", severity="error")
            return

        try:
            replace_engine = ReplaceEngine(self.book)
            if event.replace_all:
                num_replacements = replace_engine.replace_all(
                    event.find,
                    event.replace,
                    event.case_sensitive,
                    event.whole_word,
                    event.regex
                )
                self.notify(f"Made {num_replacements} replacements.", title="Replace Complete")
                self.screen_manager.pop()
            elif event.search_result:
                success = replace_engine.replace_one(event.search_result, event.replace)
                if success:
                    self.notify("Replacement successful.", title="Replace Complete")
                    self.search_results.remove(event.search_result)
                    self.screen_manager.pop()
                    self.query_one(SearchResultsScreen).refresh_results()

                else:
                    self.notify("Replacement failed.", title="Error", severity="error")
            else:
                self.notify("No action to perform.", title="Info", severity="information")

        except ValueError as e:
            self.notify(str(e), title="Replace Error", severity="error")
        except Exception as e:
            self.notify(f"An unexpected error occurred during replace: {e}", title="Error", severity="error")

    def on_batch_operations_screen_batch_operations_initiated(
        self, event: BatchOperationsScreen.BatchOperationsInitiated
    ) -> None:
        """Handle batch operations initiation."""
        if not self.book:
            self.notify("No EPUB loaded.", title="Error", severity="error")
            return

        try:
            replace_engine = ReplaceEngine(self.book)
            num_replacements = replace_engine.batch_replace_all(
                operations=event.operations,
                case_sensitive=event.case_sensitive,
                whole_word=event.whole_word,
                regex=event.regex,
            )
            self.notify(
                f"Made {num_replacements} replacements in batch operation.",
                title="Batch Replace Complete",
            )
            self.screen_manager.pop()  # Go back to dashboard
        except ValueError as e:
            self.notify(str(e), title="Batch Replace Error", severity="error")
        except Exception as e:
            self.notify(
                f"An unexpected error occurred during batch replace: {e}",
                title="Error",
                severity="error",
            )

    def action_save_book(self) -> None:
        """Saves the current book."""
        if not self.book:
            self.notify("No book loaded to save.", title="Warning", severity="warning")
            return

        if not self.book.is_modified:
            self.notify("No changes to save.", title="Info", severity="information")
            return

        try:
            saver = EpubSaver(self.book)
            saver.save()
            self.notify("Book saved successfully.", title="Success", severity="information")
        except Exception as e:
            self.notify(f"Error saving book: {e}", title="Error", severity="error")


def main():
    """Run the application."""
    app = EpsilonApp()
    app.run()

if __name__ == "__main__":
    main()

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Input, Checkbox, Button
from textual.containers import VerticalScroll, Horizontal
from textual.message import Message

from epub_editor_pro.ui.material_components import Card
from epub_editor_pro.core.search_models import SearchResult


class ReplaceScreen(Screen):
    """A screen for replacing text within the EPUB."""

    def __init__(
        self, search_result: SearchResult | None = None, *args, **kwargs
    ) -> None:
        self.search_result = search_result
        super().__init__(*args, **kwargs)

    class ReplaceInitiated(Message):
        """Posted when a replace action is initiated."""

        def __init__(
            self,
            find: str,
            replace: str,
            case_sensitive: bool,
            whole_word: bool,
            regex: bool,
            replace_all: bool,
            search_result: SearchResult | None = None,
        ) -> None:
            self.find = find
            self.replace = replace
            self.case_sensitive = case_sensitive
            self.whole_word = whole_word
            self.regex = regex
            self.replace_all = replace_all
            self.search_result = search_result
            super().__init__()

    def compose(self) -> ComposeResult:
        """Create child widgets for the screen."""
        yield Header()
        with VerticalScroll(id="replace-body"):
            yield Card(
                "Find and Replace",
                Input(placeholder="Find...", id="find-input"),
                Input(placeholder="Replace with...", id="replace-input"),
                Horizontal(
                    Checkbox("Case-sensitive", id="case-sensitive-checkbox"),
                    Checkbox("Whole word", id="whole-word-checkbox"),
                    Checkbox("Regex", id="regex-checkbox"),
                    id="replace-options"
                ),
                Horizontal(
                    Button("Replace", id="replace-button"),
                    Button("Replace All", id="replace-all-button", variant="primary"),
                    Button("Cancel", id="cancel-button"),
                    id="replace-actions"
                ),
                id="replace-card"
            )
        yield Footer()

    def on_mount(self) -> None:
        """Prefill the find input if a search result was passed."""
        if self.search_result:
            find_input = self.query_one("#find-input", Input)
            find_input.value = self.search_result.match_text

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "cancel-button":
            self.app.pop_screen()
            return

        find_query = self.query_one("#find-input", Input).value
        if not find_query:
            self.app.notify("Please enter text to find.", title="Warning", severity="warning")
            return

        replace_text = self.query_one("#replace-input", Input).value
        case_sensitive = self.query_one("#case-sensitive-checkbox", Checkbox).value
        whole_word = self.query_one("#whole-word-checkbox", Checkbox).value
        regex = self.query_one("#regex-checkbox", Checkbox).value

        if event.button.id == "replace-button":
            self.post_message(
                self.ReplaceInitiated(
                    find_query,
                    replace_text,
                    case_sensitive,
                    whole_word,
                    regex,
                    replace_all=False,
                    search_result=self.search_result,
                )
            )
        elif event.button.id == "replace-all-button":
            self.post_message(
                self.ReplaceInitiated(
                    find_query,
                    replace_text,
                    case_sensitive,
                    whole_word,
                    regex,
                    replace_all=True,
                )
            )

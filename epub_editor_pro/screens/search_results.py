from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, ListView, ListItem, Label
from textual.containers import VerticalScroll
from textual.reactive import reactive

from epub_editor_pro.core.search_models import SearchResult

class SearchResultItem(ListItem):
    """A widget to display a single search result."""

    def __init__(self, result: SearchResult) -> None:
        super().__init__()
        self.result = result

    def compose(self) -> ComposeResult:
        """Create child widgets for the list item."""
        yield Label(f"{self.result.file_path}:{self.result.line_number}", classes="file-path")
        # The rich text markup is not working as expected here.
        # I will fix this in a later step.
        yield Label(
            f"{self.result.context_before}{self.result.match_text}{self.result.context_after}",
            classes="context"
        )


class SearchResultsScreen(Screen):
    """A screen to display search results."""

    def compose(self) -> ComposeResult:
        """Create child widgets for the screen."""
        yield Header()
        with VerticalScroll(id="results-body"):
            yield ListView(id="results-list")
        yield Footer()

    def on_mount(self) -> None:
        """Called when the screen is mounted."""
        results = self.app.search_results
        list_view = self.query_one(ListView)
        for result in results:
            list_view.append(SearchResultItem(result))

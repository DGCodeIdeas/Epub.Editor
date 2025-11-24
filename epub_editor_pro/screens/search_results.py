from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, ListView, ListItem, Label
from textual.containers import VerticalScroll
from textual.message import Message

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
    class ReplaceSelection(Message):
        """Posted when the user wants to replace a single search result."""

        def __init__(self, search_result: SearchResult) -> None:
            self.search_result = search_result
            super().__init__()

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

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle the selection of a search result."""
        search_result = event.item.result
        self.post_message(self.ReplaceSelection(search_result))

    def refresh_results(self) -> None:
        """Refreshes the search results."""
        list_view = self.query_one(ListView)
        list_view.clear()
        for result in self.app.search_results:
            list_view.append(SearchResultItem(result))

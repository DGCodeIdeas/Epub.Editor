from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Label
from textual.containers import Vertical

class Dashboard(Screen):
    """The main dashboard screen."""

    def compose(self) -> ComposeResult:
        """Create child widgets for the screen."""
        yield Header()

        book = self.app.book
        if book:
            yield Vertical(
                Label(f"Title: {book.metadata.title}"),
                Label(f"Author: {book.metadata.creator}"),
                Label(f"Identifier: {book.metadata.identifier}"),
                id="dashboard-info"
            )
        else:
            yield Label("No EPUB loaded.", id="dashboard-info")

        yield Footer()

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Label
from textual.containers import VerticalScroll

from epub_editor_pro.ui.material_components import Card, Button

class Dashboard(Screen):
    """The main dashboard screen."""

    def compose(self) -> ComposeResult:
        """Create child widgets for the screen."""
        yield Header()

        book = self.app.book
        with VerticalScroll(id="dashboard-body"):
            if book:
                # Using a generator for children for cleaner code
                yield Card(
                    "File Information",
                    Label(f"Title: {book.metadata.title}"),
                    Label(f"Author(s): {', '.join(book.metadata.creator)}"),
                    Label(f"Identifier: {book.metadata.identifier}"),
                    Label(f"Language: {book.metadata.language}"),
                    Label(f"Publisher: {book.metadata.publisher}"),
                    id="file-info-card"
                )

                # Calculate statistics
                num_content_files = sum(1 for item in book.manifest.values() if "xhtml" in item.media_type)

                yield Card(
                    "Statistics",
                    Label(f"Total Files: {len(book.manifest)}"),
                    Label(f"Content Files: {num_content_files}"),
                    Label(f"Spine Items: {len(book.spine)}"),
                    Label(f"TOC Entries: {len(book.toc)}"),
                    id="stats-card"
                )

                yield Card(
                    "Quick Actions",
                    Button("Search", id="search-button"),
                    Button("Replace", id="replace-button"),
                    Button("Settings", id="settings-button"),
                    id="quick-actions-card"
                )
            else:
                yield Card("File Information", Label("No EPUB loaded."), id="file-info-card")

        yield Footer()

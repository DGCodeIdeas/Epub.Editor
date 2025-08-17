from textual.app import App, ComposeResult
from textual.widgets import Label

class EpsilonApp(App):
    """A Textual app to edit EPUBs."""

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Label("Hello, Epsilon Editor!")

def main():
    """Run the application."""
    app = EpsilonApp()
    app.run()

if __name__ == "__main__":
    main()

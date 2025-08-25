from textual.widget import Widget
from textual.containers import Grid


class ResponsiveGrid(Grid):
    """A grid that rearranges its children based on screen width."""

    def __init__(self, *children: Widget, name: str | None = None, id: str | None = None, classes: str | None = None, disabled: bool = False) -> None:
        super().__init__(*children, name=name, id=id, classes=classes, disabled=disabled)
        self.is_grid = True

    def on_resize(self, event) -> None:
        """Handle screen resize events."""
        if self.is_grid and event.size.width < 80:
            self.styles.grid_size_columns = 1
        elif self.is_grid:
            self.styles.grid_size_columns = 2

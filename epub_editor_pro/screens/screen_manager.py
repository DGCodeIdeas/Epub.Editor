from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from textual.app import App
    from textual.screen import Screen


class ScreenManager:
    """A centralized manager for screen navigation."""

    def __init__(self, app: "App"):
        """
        Initializes the ScreenManager.

        Args:
            app: The main application instance.
        """
        self._app = app

    def push(self, screen: Union[str, "Screen"]) -> None:
        """
        Pushes a new screen onto the navigation stack.

        Args:
            screen: The name of the screen to push or a Screen instance.
        """
        self._app.push_screen(screen)

    def pop(self) -> "Screen":
        """
        Pops the current screen from the stack and returns it.
        """
        return self._app.pop_screen()

    def switch_to(self, screen: Union[str, "Screen"]) -> None:
        """
        Switches to a new screen, replacing the current one.

        Args:
            screen: The name of the screen or a Screen instance to switch to.
        """
        self._app.switch_screen(screen)

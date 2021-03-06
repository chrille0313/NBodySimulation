from abc import ABC, abstractmethod

from Engine.Utils.utils import Vector2
from Engine.Utils.camera2d import Camera2D


class App(ABC):
    """
    Abstract class for module-specific applications to inherit from.

    TODO:
        - Add layers for rendering.
    """

    def __init__(self, windowSize: tuple, fps: int = 60, caption: str = "Application Window", camera: Camera2D = None):
        """
        Initialize the application.

        :param windowSize: The size of the window in pixels
        :param fps: What framerate the application should run at. Set to 0 for uncapped framerate. (default: 60)
        :param caption: The caption of the window. (default: "Game Window")
        """

        self.windowSize = Vector2(windowSize)
        self.windowCenter = Vector2(self.windowSize.x / 2, self.windowSize.y / 2)
        self._caption = caption
        self.fps = fps

        self.mainCamera = camera if camera is not None else Camera2D(Vector2(0, 0), self.windowSize)

        self.debug = False

    @property
    def caption(self) -> str:
        """
		Public property allowing sub-applications to retrieve the window caption.

		:return: The caption of the window
		"""

        return self._caption

    @caption.setter
    def caption(self, title: str) -> None:
        """
		Public setter allowing sub-applications to set the window caption.
		This setter should be overridden by module-specific applications to handle actual window caption changes.

		:param title: The new caption of the window
		:return: None
		"""

        self._caption = title

    @abstractmethod
    def __events(self):
        """
        Handle events.

        :return: None
        """

        pass

    @abstractmethod
    def __draw(self):
        """
        Draw the application.

        :return: None
        """

        pass

    @abstractmethod
    def run(self):
        """
        Run the application.

        :return: None
        """
        pass

    def draw_circle(self, pos, radius, color, borderWidth=0, fromCamera=False):
        raise NotImplementedError("draw_circle is not implemented")

    def draw_rect(self, position, width, height, color, borderWidth=0, fromCamera=False):
        raise NotImplementedError("draw_rect is not implemented")

    def draw_line(self, start, end, color, width=1, fromCamera=False):
        raise NotImplementedError("draw_line is not implemented")

    def on_update(self) -> None:
        """
        Callback for sub-applications inheriting from App.
        This is called when the application is updated.

        :return: None
        """

        pass

    def on_draw(self) -> None:
        """
        Callback for sub-applications inheriting from App.
        This is called when the application is drawn.

        :return: None
        """

        pass

    def on_quit(self) -> None:
        """
        Callback for sub-applications inheriting from App.
        This is called when the application is closed.

        :return: None
        """

        pass

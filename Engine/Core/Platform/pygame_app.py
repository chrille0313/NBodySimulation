import pygame
from Engine.Core.app import *
from Engine.colors import Colors
from Engine.constants import *


class PygameApp(App):
    """
    A wrapper class for pygame that allows for applications to more easily
    be created using custom callbacks etc.

    TODO:
        * Make keycodes in sub-applications not be dependent on pygame
        * Expose public getters for params: window, windowSize, windowCenter, clock, isKeyPressed, isMouseButtonPressed to make sure they
          cannot be set through applications
        * Add delta-time parameter
    """

    def __init__(self, windowSize: tuple, fps: int = 60, caption: str = "PyGame Window", camera: Camera2D = None):
        """
        Initializes the pygame module as well as the application.

        :param windowSize: The size of the window in pixels
        :param fps: What framerate the application should run at. Set to 0 for uncapped framerate. (default: 60)
        :param caption: The caption of the window. (default: "Game Window")
        """

        # Initialize application
        super().__init__(windowSize, fps, caption, camera)

        # Initialize pygame module
        pygame.init()
        pygame.display.set_caption(caption)
        pygame.display.set_mode(windowSize)

        # Initialize App variables
        self.window = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.deltaTime = 0
        self._running = False

        self._events = pygame.event.get()
        self.isKeyPressed = pygame.key.get_pressed()
        self.isMouseButtonPressed = pygame.mouse.get_pressed(3)

    @App.caption.setter
    def caption(self, title: str) -> None:
        """
        Public setter allowing sub-applications to set the window caption.

        :param title: The new caption of the window
        :return: None
        """

        self._caption = title
        pygame.display.set_caption(self._caption)

    @property
    def events(self) -> iter:
        """
        Public property allowing sub-applications to retrieve the events.

        :return: An iterator of events
        """

        return self._events

    def _App__events(self) -> None:
        """
        Private method for updating app events.

        :return: None
        """

        for event in self._events:
            # Make sure we can close our application
            if event.type == pygame.QUIT:
                self.quit()

            # Update what buttons are being pressed this frame
            if event.type in (pygame.KEYDOWN, pygame.KEYUP):
                self.isKeyPressed = pygame.key.get_pressed()
            elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
                self.isMouseButtonPressed = pygame.mouse.get_pressed(num_buttons=3)

        self._events = pygame.event.get()  # Update events accessible by applications

    def draw_circle(self, position, radius, color=Colors.WHITE, borderWidth=0, fromCamera=False) -> None:
        """
        Draw a circle on the screen.

        :param position: The position of the center of the circle
        :param radius: The radius of the circle
        :param color: The color of the circle
        :param borderWidth: The width of the border of the circle. Set to 0 to fill the circle. (default: 0)
        :param fromCamera: Whether or not to draw from the mainCamera's perspective. (default: False)
        :return: None
        """

        if fromCamera:
            # Draw relative to camera
            relPos = (Vector2(position) - self.mainCamera.position) * self.mainCamera.zoom
            relPos.y *= -1  # Flip y-axis (y-axis is inverted in pygame)
            relRadius = radius * self.mainCamera.zoom

            pygame.draw.circle(self.window, color, relPos + self.windowSize / 2, relRadius, borderWidth)
        else:
            pygame.draw.circle(self.window, color, position, radius, borderWidth)

    def draw_rect(self, position, width, height, color=Colors.WHITE, borderWidth=0, fromCamera=False) -> None:
        """
        Draw a rectangle on the screen.

        :param position: The position of the top left corner of the rectangle
        :param width: The width of the rectangle
        :param height: The height of the rectangle
        :param color: The color of the rectangle
        :param borderWidth: The width of the border of the rectangle. Set to 0 to fill the rectangle. (default: 0)
        :param fromCamera: Whether or not to draw from the mainCamera's perspective. (default: False)
        :return: None
        """

        if fromCamera:
            # Draw relative to camera
            relPos = (Vector2(position) - self.mainCamera.position) * self.mainCamera.zoom
            relPos.y *= -1  # Flip y-axis (y-axis is inverted in pygame)
            relWidth, relHeight = width * self.mainCamera.zoom, height * self.mainCamera.zoom

            relPos += self.windowSize / 2
            pygame.draw.rect(self.window, color, (relPos.x, relPos.y, relWidth, relHeight), borderWidth)
        else:
            pygame.draw.rect(self.window, color, (position[0], position[1], width, height), borderWidth)

    def draw_line(self, start, end, color=Colors.WHITE, width=1, fromCamera=False) -> None:
        """
        Draw a line on the screen.

        :param start: The start position of the line
        :param end: The end position of the line
        :param color: The color of the line
        :param width: The width of the line. (default: 1)
        :param fromCamera: Whether or not to draw from the mainCamera's perspective. (default: False)
        :return: None
        """

        if fromCamera:
            line = (Vector2(start, end) - self.mainCamera.position) * self.mainCamera.zoom + self.windowSize / 2
            pygame.draw.line(self.window, color, line[0], line[1], width * self.mainCamera.zoom)
        else:
            pygame.draw.line(self.window, color, start, end, width * self.mainCamera.zoom)

    def _App__draw(self) -> None:
        """
        Private method for updating the screen. Calls on_draw after clearing the screen.

        :return: None
        """

        self.window.fill(Colors.BLACK)
        self.on_draw()

        pygame.display.update()

    def quit(self) -> None:
        """
        Quit the application. Calls on_quit before quitting the application.

        :return: None
        """

        self._running = False
        self.on_quit()
        pygame.quit()

    def run(self) -> None:
        """
        Main loop for running the app. This should be called from any sub-application that uses this class.

        :return: None
        """

        self._running = True

        while self._running:
            self._App__events()  # Make sure we update the engine's events before we call on_update
            self.on_update()
            self._App__draw()
            self.deltaTime = self.clock.tick(self.fps) / 1000  # Run application on desired framerate

        self.quit()

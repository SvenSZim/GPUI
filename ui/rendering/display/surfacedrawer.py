from abc import ABC, abstractmethod

from ..utility import Color, Rect
from .surface import Surface

class SurfaceDrawer(ABC):
    """
    SurfaceDrawer is the abstract base class of all Engines that should be
    used to draw the UI on the screen.
    It defines some needed functionality which needs to be implemented as interface.
    """

    @staticmethod
    @abstractmethod
    def drawline(surface: Surface, startpoint: tuple[int, int], endpoint: tuple[int, int], color: Color) -> None:
        """
        drawline draws a line from startpoint to endpoint with the given color on the surface

        Args:
            surface    (Surface)        : the surface where the line should get drawn ontop
            startpoint (tuple[int, int]): the startpoint of the line
            endpoint   (tuple[int, int]): the endpoint of the line
            color      (Color)          : the color the line should have
        """
        pass

    @staticmethod
    @abstractmethod
    def drawrect(surface: Surface, rect: Rect, color: Color, fill: bool=True) -> None:
        """
        drawrect draws the given rect with the given color on the surface

        Args:
            surface (Surface)   : the surface where the rect should get drawn ontop
            rect    (Rect)      : the rect that should be drawn
            color   (Color)     : the color the rect should have
            fill    (bool)      : True if the rect should be of solid color (default)
                                  False if only the borders should be drawn
        """
        pass

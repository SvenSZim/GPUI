from abc import ABC, abstractmethod
from typing import Union

from ..generic import Color, Rect
from .UISurface import UISurface

class UISurfaceDrawer(ABC):
    """
    UISurfaceDrawer is the abstract base class of all Engines that should be
    used to draw the UI on the screen.
    It defines some needed functionality which needs to be implemented as interface.
    """

    @abstractmethod
    def drawline(self, surface: UISurface, startpoint: tuple[int, int], endpoint: tuple[int, int], color: Union[str, tuple[int, int, int], Color]) -> None:
        """
        drawline draws a line from startpoint to endpoint with the given color on the surface

        Args:
            surface: UISurface = the surface where the line should get drawn ontop
            startpoint: tuple[int, int] = the startpoint of the line
            endpoint: tuple[int, int] = the endpoint of the line
            color: Color = the color the line should have
        """
        pass

    @abstractmethod
    def drawrect(self, surface: UISurface, rect: Rect, color: Union[str, tuple[int, int, int], Color], fill: bool=True) -> None:
        """
        drawrect draws the given rect with the given color on the surface

        Args:
            surface: UISurface = the surface where the rect should get drawn ontop
            rect: Rect = the rect that should be drawn
            color: Color = the color the rect should have
            fill: bool = True if the rect should be of solid color (default)
                         False if only the borders should be drawn
        """
        pass

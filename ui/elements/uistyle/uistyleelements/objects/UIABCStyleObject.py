from abc import ABC, abstractmethod

from ....generic import Rect
from ....idrawer import UISurfaceDrawer, UISurface
from ..UIABCStyleElement import UIABCStyleElement


class UIABCStyleObject(UIABCStyleElement, ABC):
    """
    UIABCStyleObject is the abstract base class for all UIStyleObjects
    """
    @abstractmethod
    def render(self, surfaceDrawer: type[UISurfaceDrawer], surface: UISurface, rect: Rect) -> None:
        """
        render renders the given rect in the specific style with the given surfaceDrawer
        onto the given surface.
        """
        pass

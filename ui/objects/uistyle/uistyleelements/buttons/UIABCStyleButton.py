from abc import ABC, abstractmethod

from ....generic import Rect
from ....idrawer import UISurfaceDrawer, UISurface
from ..UIABCStyleElement import UIABCStyleElement


class UIABCStyleButton(UIABCStyleElement, ABC):
    """
    UIABCStyleButton is the abstract base class for all UIStyleButtons
    """
    @abstractmethod
    def render(self, surfaceDrawer: type[UISurfaceDrawer], surface: UISurface, rect: Rect,
               numberOfButtonStates: int, buttonState: int) -> None:
        """
        render renders the given rect in the specific style with the given surfaceDrawer
        onto the given surface.
        """
        pass

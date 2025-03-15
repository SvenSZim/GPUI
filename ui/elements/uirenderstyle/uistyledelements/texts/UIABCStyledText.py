from abc import ABC, abstractmethod
from typing import Union

from ....generic import Rect, Color
from ....uidrawerinterface import UISurfaceDrawer, UISurface, UIFont
from ..UIABCStyledElement import UIABCStyledElement


class UIABCStyledText(UIABCStyledElement, ABC):
    """
    UIABCStyleText is the abstract base class for all UIStyleText
    """
    @abstractmethod
    def render(self, surfaceDrawer: type[UISurfaceDrawer], surface: UISurface, rect: Rect, 
               content: str, font: UIFont, fontColor: Union[str, tuple[int, int, int], Color]) -> None:
        """
        render renders the given rect in the specific style with the given surfaceDrawer
        onto the given surface.
        """
        pass

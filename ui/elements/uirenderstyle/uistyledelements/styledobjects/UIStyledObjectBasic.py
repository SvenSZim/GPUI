from typing import Optional, Union, override

from ....generic import Color, Rect
from ....uidrawerinterface import UISurfaceDrawer, UISurface
from .UIABCStyledObject import UIABCStyledObject

class UIStyledObjectBasic(UIABCStyledObject):
    """
    UIStyleObjectBasic is a basic implementation of UIABCStyleObject
    """
    def __init__(self, drawBorder: tuple[bool, bool, bool, bool]=(True, True, True, True),
                 borderColor: Optional[Union[str, tuple[int, int, int], Color]]=None,
                 fillColor: Optional[Union[str, tuple[int, int, int], Color]]=None) -> None:
        super().__init__(drawBorder, borderColor, fillColor)

    @override
    def render(self, surfaceDrawer: type[UISurfaceDrawer], surface: UISurface, data: Rect) -> None:
        """
        render renders the rect as a basic rectangle with outlines
        """
        if self._fillColor is not None:
            surfaceDrawer.drawrect(surface, data, self._fillColor)
        if self._borderColor is not None:
            if self._drawBorder[0]:
                surfaceDrawer.drawline(surface, (data.left, data.top), (data.right, data.top), self._borderColor)
            if self._drawBorder[1]:
                surfaceDrawer.drawline(surface, (data.left, data.top), (data.left, data.bottom), self._borderColor)
            if self._drawBorder[2]:
                surfaceDrawer.drawline(surface, (data.right, data.top), (data.right, data.bottom), self._borderColor)
            if self._drawBorder[3]:
                surfaceDrawer.drawline(surface, (data.left, data.bottom), (data.right, data.bottom), self._borderColor)

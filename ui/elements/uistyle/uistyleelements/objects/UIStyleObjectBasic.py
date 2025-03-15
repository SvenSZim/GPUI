from typing import Optional, Union, override

from ....generic import Color, Rect
from ....idrawer import UISurfaceDrawer, UISurface
from .UIABCStyleObject import UIABCStyleObject

class UIStyleObjectBasic(UIABCStyleObject):
    """
    UIStyleObjectBasic is a basic implementation of UIABCStyleObject
    """
    __borderColor: Optional[Union[str, tuple[int, int, int], Color]]
    __fillColor: Optional[Union[str, tuple[int, int, int], Color]]
    def __init__(self, borderColor: Optional[Union[str, tuple[int, int, int], Color]]=None, fillColor: Optional[Union[str, tuple[int, int, int], Color]]=None) -> None:
        self.__borderColor = borderColor
        self.__fillColor = fillColor

    @override
    def render(self, surfaceDrawer: type[UISurfaceDrawer], surface: UISurface, rect: Rect) -> None:
        """
        render renders the rect as a basic rectangle with outlines
        """
        if self.__fillColor is not None:
            surfaceDrawer.drawrect(surface, rect, self.__fillColor)
        if self.__borderColor is not None:
            surfaceDrawer.drawrect(surface, rect, self.__borderColor, fill=False)

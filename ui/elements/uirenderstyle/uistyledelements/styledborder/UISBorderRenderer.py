from typing import Union, override

from ....generic import Color, Rect
from ....uidrawerinterface import UISurfaceDrawer, UISurface
from ..UIStyledABCRenderer import UIStyledABCRenderer
from .UISBorderData import UISBorderData

class UISBorderRenderer(UIStyledABCRenderer[UISBorderData, Rect]):


    __borderColor: Union[str, tuple[int, int, int], Color]
    __borderThickness: int

    def __init__(self, stylingData: UISBorderData, borderColor: Union[str, tuple[int, int, int], Color], borderThickness: int) -> None:
        super().__init__(stylingData)
        self.__borderColor = borderColor
        self.__borderThickness = borderThickness

    @override
    def render(self, surfaceDrawer: type[UISurfaceDrawer], surface: UISurface, renderData: Rect) -> None:
        
        #!DEBUG!
        surfaceDrawer.drawrect(surface, renderData, self.__borderColor, fill=False)

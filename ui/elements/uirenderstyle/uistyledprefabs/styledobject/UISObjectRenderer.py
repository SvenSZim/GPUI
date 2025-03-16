from typing import override

from ....generic import Rect
from ....uidrawerinterface import UISurfaceDrawer, UISurface
from ..styledborder import UISBorderRenderer
from ..UIStyledABCRenderer import UIStyledABCRenderer
from .UISObjectData import UISObjectData

class UISObjectRenderer(UIStyledABCRenderer[UISObjectData, Rect]):

    def __init__(self, stylingData: UISObjectData) -> None:
        super().__init__(stylingData)

    @override
    def render(self, surfaceDrawer: type[UISurfaceDrawer], surface: UISurface, renderData: Rect) -> None:
        
        if self._stylingData.fillColor is not None:
            surfaceDrawer.drawrect(surface, renderData, self._stylingData.fillColor)
        
        # borders:
        UISBorderRenderer(self._stylingData.borderData).render(surfaceDrawer, surface, renderData)

        # TODO: ALT

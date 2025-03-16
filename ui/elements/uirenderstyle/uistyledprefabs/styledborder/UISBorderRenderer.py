from typing import override

from ....generic import Rect
from ....uidrawerinterface import UISurfaceDrawer, UISurface
from ..UIStyledABCRenderer import UIStyledABCRenderer
from .UISBorderData import UISBorderData

class UISBorderRenderer(UIStyledABCRenderer[UISBorderData, Rect]):

    def __init__(self, stylingData: UISBorderData) -> None:
        super().__init__(stylingData)

    @override
    def render(self, surfaceDrawer: type[UISurfaceDrawer], surface: UISurface, renderData: Rect) -> None:
        
        if self._stylingData.mainColor is None:
            return

        if self._stylingData.doBorders[0]:
            surfaceDrawer.drawline(surface, 
                                   (renderData.left, renderData.top),
                                   (renderData.right, renderData.top),
                                   self._stylingData.mainColor)
        if self._stylingData.doBorders[1]:
            surfaceDrawer.drawline(surface,
                                   (renderData.left, renderData.top),
                                   (renderData.left, renderData.bottom),
                                   self._stylingData.mainColor)
        if self._stylingData.doBorders[2]:
            surfaceDrawer.drawline(surface,
                                   (renderData.right, renderData.top),
                                   (renderData.right, renderData.bottom),
                                   self._stylingData.mainColor)
        if self._stylingData.doBorders[3]:
            surfaceDrawer.drawline(surface,
                                   (renderData.left, renderData.bottom),
                                   (renderData.right, renderData.bottom),
                                   self._stylingData.mainColor)

        #TODO: ALT STATES

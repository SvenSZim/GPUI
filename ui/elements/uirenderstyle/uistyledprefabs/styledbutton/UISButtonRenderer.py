from typing import override

from ....generic import Rect
from ....uidrawerinterface import UISurfaceDrawer, UISurface
from ..styledborder import UISBorderRenderer
from ..UIStyledABCRenderer import UIStyledABCRenderer
from .UISButtonData import UISButtonData

class UISButtonRenderer(UIStyledABCRenderer[UISButtonData, tuple[Rect, int, int]]):

    def __init__(self, stylingData: UISButtonData) -> None:
        super().__init__(stylingData)

    @override
    def render(self, surfaceDrawer: type[UISurfaceDrawer], surface: UISurface, renderData: tuple[Rect, int, int]) -> None:

        rect: Rect
        numberOfStates: int
        currentState: int
        rect, numberOfStates, currentState = renderData
        
        if self._stylingData.fillColor is not None:
            surfaceDrawer.drawrect(surface, rect, self._stylingData.fillColor)

        if self._stylingData.stateDisplayColor is not None:
            activation_percent: float = currentState / (numberOfStates - 1)
            activation_width: int = int(activation_percent * rect.width)
            surfaceDrawer.drawrect(surface, Rect(rect.getPosition(), (activation_width, rect.height)), self._stylingData.stateDisplayColor)
        
        # border
        borderRenderer: UISBorderRenderer = UISBorderRenderer(self._stylingData.borderData)
        borderRenderer.render(surfaceDrawer, surface, renderData[0])


        # TODO: different activation state display styles.

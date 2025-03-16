from typing import override

from ....generic import Rect, tColor
from ....uidrawerinterface import UISurfaceDrawer, UISurface, UIFont
from ..styledborder import UISBorderRenderer
from ..UIStyledABCRenderer import UIStyledABCRenderer
from .UISTextData import UISTextData

class UISTextRenderer(UIStyledABCRenderer[UISTextData, tuple[Rect, str, UIFont, tColor]]):

    def __init__(self, stylingData: UISTextData) -> None:
        super().__init__(stylingData)

    @override
    def render(self, surfaceDrawer: type[UISurfaceDrawer], surface: UISurface, renderData: tuple[Rect, str, UIFont, tColor]) -> None:

        rect: Rect
        content: str
        font: UIFont
        fontColor: tColor
        rect, content, font, fontColor = renderData

        if self._stylingData.fillColor is not None:
            surfaceDrawer.drawrect(surface, rect, self._stylingData.fillColor)


        textRender: UISurface = font.render(content, fontColor)
        textSize: tuple[int, int] = textRender.getSize()
        textPosition: tuple[int, int] = (int(rect.getPosition()[0] + (rect.getSize()[0] - textSize[0]) / 2),
                                         int(rect.getPosition()[1] + (rect.getSize()[1] - textSize[1]) / 2))
        surface.blit(textRender, textPosition)
        
        # border
        borderRenderer: UISBorderRenderer = UISBorderRenderer(self._stylingData.borderData)
        borderRenderer.render(surfaceDrawer, surface, renderData[0])

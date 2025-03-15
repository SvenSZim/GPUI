from typing import Optional, Union, override

from ....generic import Color, Rect
from ....uidrawerinterface import UISurfaceDrawer, UISurface, UIFont
from .UIABCStyledText import UIABCStyledText

class UIStyledTextBasic(UIABCStyledText):
    """
    UIStyleTextBasic is a basic implementation of UIABCStyleText
    """
    __borderColor: Optional[Union[str, tuple[int, int, int], Color]]
    __fillColor: Optional[Union[str, tuple[int, int, int], Color]]
    def __init__(self, borderColor: Optional[Union[str, tuple[int, int, int], Color]]=None, fillColor: Optional[Union[str, tuple[int, int, int], Color]]=None) -> None:
        self.__borderColor = borderColor
        self.__fillColor = fillColor

    @override
    def render(self, surfaceDrawer: type[UISurfaceDrawer], surface: UISurface, rect: Rect, 
               content: str, font: UIFont, fontColor: Union[str, tuple[int, int, int], Color]) -> None:
        """
        render renders the rect as a basic rectangle with outlines and the font with the given specs.
        """
        if self.__fillColor is not None:
            surfaceDrawer.drawrect(surface, rect, self.__fillColor)
        if self.__borderColor is not None:
            surfaceDrawer.drawrect(surface, rect, self.__borderColor, fill=False)

        textRender: UISurface = font.render(content, fontColor)
        textSize: tuple[int, int] = textRender.getSize()
        textPosition: tuple[int, int] = (int(rect.getPosition()[0] + (rect.getSize()[0] - textSize[0]) / 2),
                                              int(rect.getPosition()[1] + (rect.getSize()[1] - textSize[1]) / 2))
        surface.blit(textRender, textPosition)

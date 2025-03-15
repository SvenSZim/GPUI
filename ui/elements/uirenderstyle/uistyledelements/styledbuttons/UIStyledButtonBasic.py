from typing import Optional, Union, override

from ....generic import Color, Rect
from ....uidrawerinterface import UISurfaceDrawer, UISurface
from .UIABCStyledButton import UIABCStyledButton

class UIStyledButtonBasic(UIABCStyledButton):
    """
    UIStyleButtonBasic is a basic implementation of UIABCStyleButton
    """
    __borderColor: Optional[Union[str, tuple[int, int, int], Color]]
    __fillColor: Optional[Union[str, tuple[int, int, int], Color]]
    __buttonStateBorderColor: Optional[Union[str, tuple[int, int, int], Color]]
    __buttonStateFillColor: Optional[Union[str, tuple[int, int, int], Color]]
    def __init__(self, borderColor: Optional[Union[str, tuple[int, int, int], Color]]=None, fillColor: Optional[Union[str, tuple[int, int, int], Color]]=None,
                 buttonStateBorderColor: Optional[Union[str, tuple[int, int, int], Color]]=None, buttonStateFillColor: Optional[Union[str, tuple[int, int, int], Color]]=None) -> None:
        self.__borderColor = borderColor
        self.__fillColor = fillColor
        self.__buttonStateBorderColor = buttonStateBorderColor
        self.__buttonStateFillColor = buttonStateFillColor

    @override
    def render(self, surfaceDrawer: type[UISurfaceDrawer], surface: UISurface, 
               data: tuple[Rect, int, int]) -> None:
        """
        render renders the rect as a basic rectangle with outlines

        Args:
            surfaceDrawer: type[UISurfaceDrawer] = the surfaceDrawer used to draw
            surface: UISurface = the surface to draw on
            data: tuple[Rect, int, int] = the rect, the numberOfButtonStates and the current buttonState.
        """
        rect, numberOfButtonStates, buttonState = data

        if self.__fillColor is not None:
            surfaceDrawer.drawrect(surface, rect, self.__fillColor)
        
        if numberOfButtonStates > 0:
            activationPercent: float = buttonState / (numberOfButtonStates - 1)
            activationRect: Rect = Rect(rect.getPosition(), (int(rect.getSize()[0] * activationPercent), rect.getSize()[1]))
            if self.__buttonStateFillColor is not None:
                surfaceDrawer.drawrect(surface, activationRect, self.__buttonStateFillColor)
            if self.__buttonStateBorderColor is not None:
                surfaceDrawer.drawrect(surface, activationRect, self.__buttonStateBorderColor, fill=False)

        if self.__borderColor is not None:
            surfaceDrawer.drawrect(surface, rect, self.__borderColor, fill=False)

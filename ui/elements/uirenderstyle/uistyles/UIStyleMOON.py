from typing import override

from ...generic import Color

from .UIABCStyle import UIABCStyle

colors: list[Color] = ['white', (205, 205, 205), (150, 150, 150)]

class UIStyleMOON(UIABCStyle):
    """
    MOON is a storage class for the UIStyleObjects of the MOON-Style
    """
    @override
    @staticmethod
    def getStyleColor(colorIndex: int) -> Color:
        return colors[colorIndex]

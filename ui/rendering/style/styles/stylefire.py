from typing import override

from ....utility import Color

from .abcstyle import ABCStyle

colors: list[Color] = ['red', 'green', (150, 150, 150)]

class StyleFIRE(ABCStyle):
    """
    StyleFIRE is a storage class for the StyleObjects of the FIRE-Style
    """
    @override
    @staticmethod
    def getStyleColor(colorIndex: int) -> Color:
        """
        getStyleColor is a method which returns the style-specific color of the given index

        Args:
            colorIndex (int): the index of the color

        Returns (Color): the requested Color
        """
        return colors[colorIndex]

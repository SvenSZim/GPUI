
from ...utility import Color
from .styles import ABCStyle, StyleMOON, StyleFIRE
from .renderstyle import RenderStyle

class StyleManager:
    """
    StyleManager is a class to manage the render-data-requests for renderstyles    
    """

    @staticmethod
    def __mapStyle(style: RenderStyle) -> ABCStyle:
        """
        mapStyle is an intern method to map the style-data object to the actual
        style container class.
        """
        return {RenderStyle.MOON: StyleMOON,
                RenderStyle.FIRE: StyleFIRE}[style]
    
    @staticmethod
    def getStyleColor(colorIndex: int, style: RenderStyle) -> Color:
        """
        getStyleColor is a requst method to get renderstyle-specific color information.

        Args:
            colorIndex (int)    : the index of the requested color
            style      (style)  : the style for which the color is requested

        Returns (Color): the requested color from the specified style
        """
        return StyleManager.__mapStyle(style).getStyleColor(colorIndex)

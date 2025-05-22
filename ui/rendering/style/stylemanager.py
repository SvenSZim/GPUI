import json
import os

from ...utility import Color, tColor
from .renderstyle import RenderStyle

styledata: dict

filepath: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'styles.json')
with open(filepath,'r') as file:
    styledata = json.load(file)


class StyleManager:
    """
    StyleManager is a class to manage the render-data-requests for renderstyles    
    """

    @staticmethod
    def __mapStyle(style: RenderStyle) -> list[str]:
        """
        mapStyle is an intern method to map the style-data object to the actual
        style container class.
        """
        return styledata[{RenderStyle.NONE: "none",
                RenderStyle.MOON: "moon",
                RenderStyle.FIRE: "fire"}[style]]
    
    @staticmethod
    def getStyleColor(colorIndex: int, style: RenderStyle) -> Color:
        """
        getStyleColor is a requst method to get renderstyle-specific color information.

        Args:
            colorIndex (int)    : the index of the requested color
            style      (style)  : the style for which the color is requested

        Returns (Color): the requested color from the specified style
        """
        colors: list[str] = StyleManager.__mapStyle(style)
        if colorIndex >= len(colors):
            return (0, 0, 0)
        return tColor(colors[colorIndex])

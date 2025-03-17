
from ..generic import Color
from .uistyles import UIABCStyle, UIStyleMOON, UIStyleFIRE
from .UIStyle import UIStyle

class UIStyleManager:

    @staticmethod
    def __mapStyle(style: UIStyle) -> UIABCStyle:
        return {UIStyle.MOON: UIStyleMOON,
                UIStyle.FIRE: UIStyleFIRE}[style]
    
    @staticmethod
    def getStyleColor(colorIndex: int, style: UIStyle) -> Color:
        return UIStyleManager.__mapStyle(style).getStyleColor(colorIndex)

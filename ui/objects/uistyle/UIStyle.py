from enum import Enum

from .uistyleelements import UIABCStyleElement, UIStyleElements
from .uistyleelements import UIStyleColor, UIStyleBasicRect

class UIStyle(Enum):
    MOON = 0

    def getStyleElement(self, styleElement: UIStyleElements) -> UIABCStyleElement:
        match self:
            case UIStyle.MOON:
                return UIStyle.getMoonStyleElement(styleElement)


    @staticmethod
    def getMoonStyleElement(styleElement: UIStyleElements) -> UIABCStyleElement:
        match styleElement:
            case UIStyleElements.COLOR:
                return UIStyleColor('white')

            case UIStyleElements.COLOR1:
                return UIStyleColor('blue')

            case UIStyleElements.COLOR2:
                return UIStyleColor('red')

            case UIStyleElements.BASIC_RECT:
                return UIStyleBasicRect()

            case UIStyleElements.ADANCED_RECT:
                return UIStyleBasicRect()
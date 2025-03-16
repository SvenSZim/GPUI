
from .uistyledprefabs import UISObject, UISObjectRenderer
from .uistyledprefabs import UISText, UISTextRenderer
from .uistyledprefabs import UISButton, UISButtonRenderer
from .uistyles import UIABCStyle, UIStyleMOON, UIStyleFIRE
from .UIStyle import UIStyle

class UIStyleManager:

    @staticmethod
    def __mapStyle(style: UIStyle) -> UIABCStyle:
        return {UIStyle.MOON: UIStyleMOON,
                UIStyle.FIRE: UIStyleFIRE}[style]
    
    @staticmethod
    def getStyledObject(objectPrefabSpecifier: UISObject, style: UIStyle) -> UISObjectRenderer:
        return UIStyleManager.__mapStyle(style).getStyledObject(objectPrefabSpecifier)

    @staticmethod
    def getStyledText(textPrefabSpecifier: UISText, style: UIStyle) -> UISTextRenderer:
        return UIStyleManager.__mapStyle(style).getStyledText(textPrefabSpecifier)

    @staticmethod
    def getStyledButton(buttonPrefabSpecifier: UISButton, style: UIStyle) -> UISButtonRenderer:
        return UIStyleManager.__mapStyle(style).getStyledButton(buttonPrefabSpecifier)



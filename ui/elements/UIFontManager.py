from .uidrawerinterface import UIFont

class UIFontManager:

    __font: type[UIFont] | None = None

    @staticmethod
    def setFont(font: type[UIFont]) -> None:
        UIFontManager.__font = font


    @staticmethod
    def getFont() -> type[UIFont]:
        if UIFontManager.__font is None:
            raise ValueError("UIFontManager::font is not instantiated!")
        return UIFontManager.__font

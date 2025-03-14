from .idrawer import UIFont

class UIFontManager:

    __font: UIFont | None = None

    @staticmethod
    def setFont(font: UIFont) -> None:
        UIFontManager.__font = font


    @staticmethod
    def getFont() -> UIFont:
        if UIFontManager.__font is None:
            raise ValueError("UIFontManager::font is not instantiated!")
        return UIFontManager.__font
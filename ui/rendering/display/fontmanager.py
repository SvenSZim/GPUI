from .font import Font

class FontManager:
    """
    FontManager is the ui's manager of the current implementation
    of the Font interface specified by this module.
    """

    __font: type[Font] | None = None # the current implementation of Font

    @staticmethod
    def setFont(font: type[Font]) -> None:
        """
        setFont sets the current active Font-implementation

        Args:
            font (type[Font]): the Font-implementation to be set.
        """
        FontManager.__font = font


    @staticmethod
    def getFont() -> type[Font]:
        """
        getFont returns the current active Font-implementation of the ui.

        Returns (type[Font]): the current active Font-implementation
        """
        if FontManager.__font is None:
            raise ValueError("FontManager::font is not instantiated!")
        return FontManager.__font

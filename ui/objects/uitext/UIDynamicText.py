from typing import Union, override

from ..generic import Color
from ..idrawer import UISurfaceDrawer, UISurface, UIFont
from ..uistyle import UIABCStyle, UIStyleTexts
from ..UIFontManager import UIFontManager

from .UIABCText import UIABCTextRenderer
from .UIText import UIText


class UIDynamicTextRenderer(UIABCTextRenderer):
    """
    UIDynamicTextRender is a UITextRender which dynamically scales the fontsize
    with the box-size, text-length and font type.
    """

    def __init__(self, core: UIText, 
                       fontName: str, fontColor: Union[str, tuple[int, int, int], Color],
                       active: bool=True) -> None:
        """
        __init__ initializes the UIDynamicTextRender instance

        Args:
            core: UIText = the refering UIText
            fontName: str = the systemfont name of used font
            fontColor: Color = the color the font should have
            active: bool = the active-state of the UIDynamicTextRenderer
        """
        fontSize: int = self.__getDynamicFontSize(fontName, core.getSize(), core.getContent())
        font: UIFont = UIFontManager.getFont().SysFont(fontName, fontSize)
        super().__init__(core, fontName, fontSize, font, fontColor, active)

    @override
    def updateFont(self) -> None:
        """
        updateFont updates the font of the UIDynamicTextRender used for render
        depending on the text-content, box-size and font type.
        """
        self._fontSize = self.__getDynamicFontSize(self._fontName, self._core.getSize(), self._core.getContent())
        self._font = UIFontManager.getFont().SysFont(self._fontName, self._fontSize)


    @staticmethod
    def __getDynamicFontSize(fontName: str, boxSize: tuple[int, int], text: str) -> int:
        """
        getDynamicFont calculates the maximal fontsize to use for the given SysFont
        to still make the given text fit in the given box

        Args:
            fontName: str = the SysFont name to use
            boxSize: tuple[int, int]: the size of the box the text should fit in
            text: str = the text to fit in the box

        Returns:
            int = the maximal fontsize to still fit in the box
        """

        def text_fits_in_box(textRender: UISurface) -> bool:
            nonlocal boxSize
            textSize: tuple[int, int] = textRender.getSize()
            return (boxSize[0] > textSize[0]) and (boxSize[1] > textSize[1])

        start_search: int = 0
        end_search: int = min(boxSize)
        while start_search < end_search:
            mid_search: int = int((start_search + end_search) / 2)
        
            test_font = UIFontManager.getFont().SysFont(fontName, mid_search)
            test_render: UISurface = test_font.render(text, (255, 255, 255))

            if text_fits_in_box(test_render):
                start_search = mid_search + 1
            else: 
                end_search = mid_search - 1

        return start_search
    

    @override
    def render(self, surfaceDrawer: type[UISurfaceDrawer], surface: UISurface) -> None:
        """
        render renders the UIObject onto the given surface

        Args:
            surfaceDrawer: UISurfaceDrawer = the drawer to use when drawing on surface
            surface: UISurface = the surface the UIObject should be drawn on
        """

        # check if UIElement should be rendered
        if not self._active:
            return


        surfaceDrawer.drawrect(surface, self._core.getRect(), 'white', fill=False)

        textRender: UISurface = self._font.render(self._core.getContent(), self._fontColor)
        textSize: tuple[int, int] = textRender.getSize()
        textPosition: tuple[int, int] = (int(self._core.getPosition()[0] + (self._core.getSize()[0] - textSize[0]) / 2),
                                              int(self._core.getPosition()[1] + (self._core.getSize()[1] - textSize[1]) / 2))
        surface.blit(textRender, textPosition)


    @override
    def renderStyled(self, surfaceDrawer: type[UISurfaceDrawer], surface: UISurface, renderStyle: type[UIABCStyle]) -> None:
        if not self._active:
            return
        
        if self._renderStyleElement is None:
            renderStyle.getStyledText(UIStyleTexts.BASIC).render(surfaceDrawer, surface, self._core.getRect(), self._core.getContent(), self._font, self._fontColor)
        else:
            renderStyle.getStyledText(self._renderStyleElement).render(surfaceDrawer, surface, self._core.getRect(), self._core.getContent(), self._font, self._fontColor)



from typing import Union, override

from ..generic import Color
from ..idrawer import UISurfaceDrawer, UISurface, UIFont
from ..uistyle import UIABCStyle, UIStyleTexts
from ..UIFontManager import UIFontManager

from .UIText import UIText
from .UIABCText import UIABCTextRenderer

class UIStaticTextRenderer(UIABCTextRenderer):
    """
    UIStaticTextRender is a UITextRender which has a fixed used font for rendering.
    """

    def __init__(self, core: UIText,
                       fontName: str='Arial', fontSize: int=10, fontColor: Union[str, tuple[int, int, int], Color]=Color('white'),
                       active: bool=True) -> None:
        """
        __init__ initializes the UIDynamicTextRender instance

        Args:
            body: UIText = the refering UIText
            fontName: str = the systemfont name of used font
            fontSize: int = the used fonsize
            fontColor: Color = the color the font should have
            active: bool = the active-state of the UIDynamicTextRenderer
        """
        
        font: UIFont = UIFontManager.getFont().SysFont(fontName, fontSize)
        super().__init__(core, fontName, fontSize, font, fontColor, active)

    def updateFont(self) -> None:
        """
        updateFont updates the font used for rendering.
        In UIStaticTextRender the fontsize does not scale with the box-size or the text-content.
        """
        self._font = UIFontManager.getFont().SysFont(self._fontName, self._fontSize)


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




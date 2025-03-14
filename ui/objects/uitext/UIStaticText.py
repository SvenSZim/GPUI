from typing import override

from ..generic import Color
from ..idrawer import UISurface
from ..UIFontManager import UIFontManager

from .UIText import UIText
from .UIABCText import UIABCTextRenderer

class UIStaticTextRenderer(UIABCTextRenderer):
    """
    UIStaticTextRender is a UITextRender which has a fixed used font for rendering.
    """

    def __init__(self, body: UIText,
                       fontName: str='Arial', fontSize: int=10, fontColor: Color=Color('white'),
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
        self.active = active
        self.body = body

        self.fontName = fontName
        self.fontSize = fontSize
        self.fontColor = fontColor

        self.updateFont()

    def updateFont(self) -> None:
        """
        updateFont updates the font used for rendering.
        In UIStaticTextRender the fontsize does not scale with the box-size or the text-content.
        """
        self._font = UIFontManager.getFont().SysFont(self.fontname, self.fontsize)

    @override
    def renderer(self, surface: UISurface) -> None:
        """
        render renders the UIObject onto the given surface

        Args:
            surface: UISurface = the surface the UIObject should be drawn on
        """

        # check if UIElement should be rendered
        if not self.active:
            return


        UIRenderer.getRenderStyle().getStyleElement(UIStyleElements.BASIC_RECT).render(UIRenderer.getDrawer(), surface, self.getUIObject().getRect())

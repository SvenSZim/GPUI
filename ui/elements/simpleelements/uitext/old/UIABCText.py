from abc import ABC
from typing import Optional, Generic, TypeVar


from ...generic import tColor, Rect
from ...uidrawerinterface import UIFont, UISurface, UISurfaceDrawer
from ...uirenderstyle import UIStyleManager, UIStyle, UISText

from ..uielementbody import UIABCBody, UIStaticBody
from ..UIABC import UIABC
from ..UIABCRenderer import UIABCRenderer

class UIABCText(UIABC[UIABCBody], ABC):
    """
    UIABCText is the abstract base class for all UIText.
    """
    
    _content: str # text-content

    def __init__(self, body: UIABCBody | Rect, content: str) -> None:
        """
        __init__ initializes thed values of UIABCText for the UITextElement

        Args:
            body: UIABCBody = the body of the UITextElement
            content: str = the text-content of the UITextElement
        """
        if isinstance(body, Rect):
            body = UIStaticBody(body)
        super().__init__(body)
        self._content = content

    def getContent(self) -> str:
        """
        getContent returns the text-content of the UIText.

        Returns:
            str = text-content of the UIText
        """
        return self._content

    def setContent(self, content: str) -> None:
        """
        setContent sets the text-content of the UIText to a new given text-content.

        Args:
            content: str = new text-content for the UIText
        """
        self._content = content



Core = TypeVar('Core', bound=UIABCText)

class UIABCTextRenderer(Generic[Core], UIABCRenderer[Core, UISText], ABC):
    """
    UIABCTextRender is the abstract base class for all UITextRender
    """
    _fontColor: tColor
    _font: UIFont

    def __init__(self, core: Core, 
                 font: UIFont, fontColor: tColor,
                 active: bool, renderStyleText: Optional[UISText]) -> None:
        """
        __init__ initializes the UIDynamicTextRender instance

        Args:
            core: Core (bound=UIABCText) = the refering UITextElement (for UIABCRenderer)
            fontName: str = the systemfont name of used font
            fontSize: int = the fontsize of the font
            font: UIFont = the font used
            fontColor: Color = the color the font should have
            active: bool = the active-state of the UITextElementRenderer (for UIABCRenderer)
            renderStyleText: UIStyledTexts = the render style that should be used when rendering styled
        """
        super().__init__(core, active, renderStyleText)
        self._font = font
        self._fontColor = fontColor


    def updateContent(self, content: str) -> None:
        """
        update Content updates the str-content of the refering UITextElement.
        """
        self._core.setContent(content)

    
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


    def renderStyled(self, surfaceDrawer: type[UISurfaceDrawer], surface: UISurface, renderStyle: UIStyle) -> None:
        if not self._active:
            return
        
        if self._renderStyleElement is None:
            UIStyleManager.getStyledText(UISText.BASIC, renderStyle).render(surfaceDrawer, surface, (self._core.getRect(), self._core.getContent(), self._font, self._fontColor))
        else:
            UIStyleManager.getStyledText(self._renderStyleElement, renderStyle).render(surfaceDrawer, surface, (self._core.getRect(), self._core.getContent(), self._font, self._fontColor))



from abc import ABC, abstractmethod
from typing import Union, override, Generic, TypeVar


from ..generic import Color
from ..idrawer import UIFont
from ..uistyle import UIStyleTexts

from ..uiobjectbody import UIABCBody
from ..UIABC import UIABC
from ..UIABCRenderer import UIABCRenderer

class UIABCText(UIABC[UIABCBody], ABC):
    """
    UIABCText is the abstract base class for all UIText.
    """
    
    _content: str # text-content

    def __init__(self, body: UIABCBody, content: str) -> None:
        """
        __init__ initializes thed values of UIABCText for the UITextElement

        Args:
            body: UIABCBody = the body of the UITextElement
            content: str = the text-content of the UITextElement
        """
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

class UIABCTextRenderer(Generic[Core], UIABCRenderer[Core, UIStyleTexts], ABC):
    """
    UIABCTextRender is the abstract base class for all UITextRender
    """
    _fontName: str
    _fontColor: Union[str, tuple[int, int, int], Color]
    _fontSize: int
    _font: UIFont

    def __init__(self, core: Core, 
                       fontName: str, fontSize: int, 
                       font: UIFont, fontColor: Union[str, tuple[int, int, int], Color], 
                       active: bool=True) -> None:
        """
        __init__ initializes the UIDynamicTextRender instance

        Args:
            core: Core (bound=UIABCText) = the refering UITextElement (for UIABCRenderer)
            fontName: str = the systemfont name of used font
            fontSize: int = the fontsize of the font
            font: UIFont = the font used
            fontColor: Color = the color the font should have
            active: bool = the active-state of the UITextElementRenderer (for UIABCRenderer)
        """
        super().__init__(core, active)
        self._fontName = fontName
        self._fontColor = fontColor
        self._fontSize = fontSize
        self._font = font


    @abstractmethod
    def updateFont(self) -> None:
        """
        updateFont updates the font of the UIABCTextRender used for rendering.
        """
        pass


    def updateContent(self, content: str) -> None:
        """
        update Content updates the str-content of the refering UITextElement.
        """
        self._core.setContent(content)
        self.updateFont()


    @override
    def update(self) -> None:
        """
        update extends the update from UIABCRenderer to also update the font.
        """
        super().update()
        self.updateFont()




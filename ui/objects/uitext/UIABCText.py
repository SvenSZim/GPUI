from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import override

from ..idrawer import UIFont
from ..uiobject import UIABCObject

class UIABCText(UIABCObject, ABC):
    """
    UIABCText is the abstract base class for all UIText.
    """
    
    content: str # text-content

    def getContent(self) -> str:
        """
        getContent returns the text-content of the UIText.

        Returns:
            str = text-content of the UIText
        """
        return self.content

    def setContent(self, content: str) -> None:
        """
        setContent sets the text-content of the UIText to a new given text-content.

        Args:
            content: str = new text-content for the UIText
        """
        self.content = content



from ..generic import Color
from ..uiobject import UIABCObjectRender, UIABCObjectRenderInfo

@dataclass
class UIABCTextRenderInfo(UIABCObjectRenderInfo, ABC):
    """
    UIABCTextRenderInfo is the abstract base class for all UITextRenderInfo
    """
    
    fontName: str = 'Arial'
    fontColor: Color = Color('white')
    fontSize: int = 10
    font: UIFont = UIFont.SysFont(fontName, fontSize)

class UIABCTextRender(UIABCObjectRender[UIABCText, UIABCTextRenderInfo], ABC):
    """
    UIABCTextRender is the abstract base class for all UITextRender
    """
    @abstractmethod
    def updateFont(self) -> None:
        """
        updateFont updates the font of the UIABCTextRender used for rendering
        """
        pass


    @override
    def update(self) -> None:
        """
        update updates the position and sizing of the UIElement and the font.
        """
        self.body.update()
        self.updateFont()

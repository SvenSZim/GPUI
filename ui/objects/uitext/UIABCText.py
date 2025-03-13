from abc import ABC
from dataclasses import dataclass

from ..idrawer import UIFont
from ..uiobject import UIABCObject

class UIABCText(UIABCObject, ABC):
    
    content: str

    def getContent(self) -> str:
        return self.content

    def setContent(self, content: str) -> None:
        self.content = content



from ..generic import Color
from ..uiobject import UIABCObjectRender, UIABCObjectRenderInfo

@dataclass
class UIABCTextRenderInfo(UIABCObjectRenderInfo):
    
    fontName: str = 'Arial'
    fontColor: Color = Color('white')
    fontSize: int = 10
    font: UIFont = UIFont.SysFont(fontName, fontSize)

class UIABCTextRender(UIABCObjectRender[UIABCText, UIABCTextRenderInfo], ABC):
    pass

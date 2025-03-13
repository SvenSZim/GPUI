
from dataclasses import dataclass
from typing import override

from ..uiobjectbody import UIABCBody
from ..uiobject import UIABCObject
from .UIABCText import UIABCText

class UIStaticText(UIABCText):

    def __init__(self, objectBody: UIABCBody, content: str, active: bool=True) -> None:
        self.active = active
        self.body = objectBody
        UIABCObject.update(self) #explicitly calls the update function from UIObject (in case it gets overwritten)

        self.content = content
 

from ..idrawer import UIFont
from .UIABCText import UIABCTextRenderInfo, UIABCTextRender

@dataclass
class UIStaticTextRenderInfo(UIABCTextRenderInfo):
    pass

class UIStaticTextRender(UIABCTextRender):

    def __init__(self, body: UIStaticText, renderInfo: UIStaticTextRenderInfo) -> None:
        self.body = body
        self.renderInfo = renderInfo

        self.updateFont()

    def updateFont(self) -> None:
        fontname = self.renderInfo.fontName
        fontsize = self.renderInfo.fontSize
        self.renderInfo.font = UIFont.SysFont(fontname, fontsize)
 
    @override
    def update(self) -> None:
        self.body.update()
        self.updateFont()

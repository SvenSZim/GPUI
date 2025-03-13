from dataclasses import dataclass
from typing import override

from ..uiobjectbody import UIABCBody
from ..uiobject import UIABCObject
from .UIABCText import UIABCText

class UIDynamicText(UIABCText):

    def __init__(self, objectBody: UIABCBody, content: str, active: bool=True) -> None:
        self.active = active
        self.body = objectBody
        UIABCObject.update(self) #explicitly calls the update function from UIObject (in case it gets overwritten)

        self.content = content
 

from ..idrawer import UISurface
from ..UIRenderer import UIRenderer
from .UIABCText import UIABCTextRenderInfo, UIABCTextRender

@dataclass
class UIDynamicTextRenderInfo(UIABCTextRenderInfo):
    pass

class UIDynamicTextRender(UIABCTextRender):

    def __init__(self, body: UIDynamicText, renderInfo: UIDynamicTextRenderInfo) -> None:
        self.body = body
        self.renderInfo = renderInfo

        self.updateFont()

    def updateFont(self) -> None:
        content = self.body.getContent()
        fontname = self.renderInfo.fontName
        self.renderInfo.font = UIRenderer.font.SysFont(fontname, get_optimal_font_size(self.body.getSize(), fontname, content))
 
    @override
    def update(self) -> None:
        self.body.update()
        self.updateFont()






def get_optimal_font_size(max_size: tuple[int, int], sysfont_name: str, text: str) -> int:
    
    def text_fits_in_box(max_size: tuple[int, int], text_size: tuple[int, int]) -> bool:
        return (max_size[0] > text_size[0]) and (max_size[1] > text_size[1])

    start_search: int = 0
    end_search: int = min(max_size)
    while start_search < end_search:
        mid_search: int = int((start_search + end_search) / 2)
        
        test_font = UIRenderer.font.SysFont(sysfont_name, mid_search)
        test_render: UISurface = test_font.render(text, (255, 255, 255))
        test_size: tuple[int, int] = test_render.getSize()

        if text_fits_in_box(max_size, test_size):
            start_search = mid_search + 1
        else: 
            end_search = mid_search - 1

    return start_search

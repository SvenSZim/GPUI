from dataclasses import dataclass
from typing import override

from ..idrawer import UISurface
from ..UIRenderer import UIRenderer
from .UIABCText import UIABCTextRenderInfo, UIABCTextRender
from .UIText import UIText

@dataclass
class UIDynamicTextRenderInfo(UIABCTextRenderInfo):
    """
    UIDynamicTextRenderInfo is the UIRenderInfo for the UIDynamicTextRender
    """
    pass

class UIDynamicTextRender(UIABCTextRender):
    """
    UIDynamicTextRender is a UITextRender which dynamically scales the fontsize
    with the box-size, text-length and font type.
    """

    def __init__(self, body: UIText, renderInfo: UIDynamicTextRenderInfo) -> None:
        """
        __init__ initializes the UIDynamicTextRender instance

        Args:
            body: UIText = the refering UIText
            renderInfo: UIDynamicTextRenderInfo = the UIRenderInfo used for rendering the UIDynamicTextRender
        """
        self.body = body
        self.renderInfo = renderInfo

        self.updateFont()

    @override
    def updateFont(self) -> None:
        """
        updateFont updates the font of the UIDynamicTextRender used for render
        depending on the text-content, box-size and font type.
        """
        content = self.getUIObject().getContent()
        fontname = self.getUIRenderInfo().fontName
        self.getUIRenderInfo().font = UIRenderer.font.SysFont(fontname, get_maximal_font_size(self.body.getSize(), fontname, content))






def get_maximal_font_size(max_size: tuple[int, int], sysfont_name: str, text: str) -> int:
    
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

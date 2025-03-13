
from dataclasses import dataclass
from typing import override

from .UIText import UIText

from ..idrawer import UIFont
from .UIABCText import UIABCTextRenderInfo, UIABCTextRender

@dataclass
class UIStaticTextRenderInfo(UIABCTextRenderInfo):
    """
    UIStaticTextRenderInfo is the UIRenderInfo for the UIStaticTextRenderer
    """
    pass

class UIStaticTextRender(UIABCTextRender):
    """
    UIStaticTextRender is a UITextRender which has a fixed used font for rendering.
    """

    def __init__(self, body: UIText, renderInfo: UIStaticTextRenderInfo) -> None:
        """
        __init__ initializes the UIStaticTextRender instance

        Args:
            body: UIText = the refering UIText
            renderInfo: UIStaticTextRenderInfo = the UIRenderInfo used for rendering the UIStaticTextRender
        """
        self.body = body
        self.renderInfo = renderInfo

        self.updateFont()

    def updateFont(self) -> None:
        """
        updateFont updates the font used for rendering.
        In UIStaticTextRender the fontsize does not scale with the box-size or the text-content.
        """
        fontname = self.getUIRenderInfo().fontName
        fontsize = self.getUIRenderInfo().fontSize
        self.getUIRenderInfo().font = UIFont.SysFont(fontname, fontsize)

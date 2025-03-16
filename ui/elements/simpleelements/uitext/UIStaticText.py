from typing import Optional

from ...generic import tColor
from ...uidrawerinterface import UIFont
from ...uirenderstyle import UISText
from ...UIFontManager import UIFontManager

from .UIText import UIText
from .UIABCText import UIABCTextRenderer

class UIStaticTextRenderer(UIABCTextRenderer):
    """
    UIStaticTextRender is a UITextRender which has a fixed used font for rendering.
    """

    def __init__(self, core: UIText,
                       fontInfo: UIFont | tuple[str, int], fontColor: tColor,
                       active: bool=True, renderStyleText: Optional[UISText]=None) -> None:
        """
        __init__ initializes the UIDynamicTextRender instance

        Args:
            body: UIText = the refering UIText
            fontInfo: UIFont | tuple[str, int] = either the font to use of the font-name and font-size to use
            fontColor: Color = the color the font should have
            active: bool = the active-state of the UIDynamicTextRenderer
            renderStyleText: UIStyledTexts = the render style that should be used when rendering styled
        """
        if isinstance(fontInfo, tuple):
            super().__init__(core, UIFontManager.getFont().SysFont(fontInfo[0], fontInfo[1]), fontColor, active, renderStyleElement)
        else:
            super().__init__(core, fontInfo, fontColor, active, renderStyleText)

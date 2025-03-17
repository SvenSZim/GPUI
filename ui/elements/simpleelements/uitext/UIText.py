from typing import override

from ...generic import Rect
from ...uidrawerinterface import UISurface, UIFont
from ...UIFontManager import UIFontManager

from ..uiobject import UIObject
from ..UIABC import UIABC
from .UITextCore import UITextCore
from .UISText import UISText
from .UISTextCreateOptions import UISTextCreateOptions
from .UITextRenderData import UITextRenderData
from .UISTextCreator import UISTextCreator
from .UISTextPrefabs import UISTextPrefabs


class UIText(UIABC[UITextCore, UITextRenderData]):
    """
    UITextRender is the UIElementRender for all UITexts.
    """

    def __init__(self, core: UITextCore, active: bool=True, renderStyleData: UISText | list[UISTextCreateOptions] | UITextRenderData=UISText.BASIC) -> None:
        """
        __init__ initializes the UITextRender instance

        Args:
            core: UIText | UIABCBody | Rect = the refering UIText (Or UIABCBody bcs. they are 'equivalet')
            active: bool = active-state of the UITextRenderer
            renderStyleElement: UIStyledTexts = the render style that should be used when rendering styled
        """
        assert self._renderstyle is not None

        if isinstance(renderStyleData, UISText):
            renderStyleData = UISTextPrefabs.getPrefabRenderData(renderStyleData, self._renderstyle)
        elif isinstance(renderStyleData, list):
            renderStyleData = UISTextCreator.createStyledElement(renderStyleData, self._renderstyle)
        
        super().__init__(core, active, renderStyleData)
        self.updateContent(self._core.getContent())

    
    def updateContent(self, content: str) -> None:
        self._core.setContent(content)
        if self._renderData.dynamicText:
            self._renderData.fontSize = getDynamicFontSize(self._renderData.sysFontName, self._core.getBody().getRect().getSize(), content)


    @override
    def render(self, surface: UISurface) -> None:
        """
        render renders the UIText onto the given surface

        Args:
            surface: UISurface = the surface the UIText should be drawn on
        """
        assert self._drawer is not None

        rect: Rect = self._core.getBody().getRect()

        # check if UIElement should be rendered
        if not self._active:
            return

        # draw object
        drawObject: UIObject = UIObject(rect, renderStyleData=self._renderData.objectData)
        
        drawObject.renderFill(surface)
        
        if self._renderData.textColor is not None and self._renderData.fontSize is not None:
                
            font: UIFont = UIFontManager.getFont().SysFont(self._renderData.sysFontName, self._renderData.fontSize)
            text_render: UISurface = font.render(self._core.getContent(), self._renderData.textColor)
            text_size: tuple[int, int] = text_render.getSize()
            text_position: tuple[int, int] = (int(rect.getPosition()[0] + (rect.getSize()[0] - text_size[0]) / 2),
                                                  int(rect.getPosition()[1] + (rect.getSize()[1] - text_size[1]) / 2))
            surface.blit(text_render, text_position)

        drawObject.renderBorders(surface)


def getDynamicFontSize(font_name: str, box_size: tuple[int, int], text: str) -> int:
    """
    getDynamicFont calculates the maximal fontsize to use for the given SysFont
    to still make the given text fit in the given box

    Args:
        font_name: str = the SysFont name to use
        box_size: tuple[int, int]: the size of the box the text should fit in
        text: str = the text to fit in the box

    Returns:
        int = the maximal fontsize to still fit in the box
    """

    def text_fits_in_box(text_render: UISurface) -> bool:
        nonlocal box_size
        text_size: tuple[int, int] = text_render.getSize()
        return (box_size[0] > text_size[0]) and (box_size[1] > text_size[1])

    start_search: int = 0
    end_search: int = min(box_size)
    while start_search < end_search:
        mid_search: int = int((start_search + end_search) / 2)
        
        test_font = UIFontManager.getFont().SysFont(font_name, mid_search)
        test_render: UISurface = test_font.render(text, (255, 255, 255))

        if text_fits_in_box(test_render):
            start_search = mid_search + 1
        else: 
            end_search = mid_search - 1

    return start_search

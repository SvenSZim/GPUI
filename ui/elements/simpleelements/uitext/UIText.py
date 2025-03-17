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
        UIObject(rect, renderStyleData=self._renderData.objectData).render(surface)

        
        if self._renderData.textColor is not None:
            if self._renderData.dynamicText:
                # calculate textsize dynamically
                pass
            else:
                assert self._renderData.fontSize is not None
                
                font: UIFont = UIFontManager.getFont().SysFont(self._renderData.sysFontName, self._renderData.fontSize)
                text_render: UISurface = font.render(self._core.getContent(), self._renderData.textColor)
                text_size: tuple[int, int] = text_render.getSize()
                text_position: tuple[int, int] = (int(rect.getPosition()[0] + (rect.getSize()[0] - text_size[0]) / 2),
                                                  int(rect.getPosition()[1] + (rect.getSize()[1] - text_size[1]) / 2))
                surface.blit(text_render, text_position)



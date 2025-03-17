from typing import Optional, override

from ...generic import Rect, Color
from ...uidrawerinterface import UISurface
from ...uirenderstyle import UIStyle

from ..uielementbody import UIABCBody
from ..UIABC import UIABC
from .UILineCore import UILineCore
from .UILineRenderData import UILineRenderData
from .UISLine import UISLine
from .UISLineCreateOptions import UISLineCreateOptions
from .UISLineCreator import UISLineCreator
from .UISLinePrefabs import UISLinePrefabs


class UILine(UIABC[UILineCore, UILineRenderData]):
    """
    UILineRender is the UIElementRender for all UILines.
    """

    def __init__(self, core: UILineCore | UIABCBody | Rect, active: bool=True, renderStyleData: UISLine | list[UISLineCreateOptions] | UILineRenderData=UISLine.SOLID) -> None:
        """
        __init__ initializes the UILineRender instance

        Args:
            core: UILine | UIABCBody | Rect = the refering UILine (Or UIABCBody bcs. they are 'equivalet')
            active: bool = active-state of the UILineRenderer
            renderStyleElement: UIStyledTexts = the render style that should be used when rendering styled
        """
        assert self._renderstyle is not None

        if not isinstance(core, UILineCore):
            core = UILineCore(core)

        if isinstance(renderStyleData, UISLine):
            renderStyleData = UISLinePrefabs.getPrefabRenderData(renderStyleData, self._renderstyle)
        elif isinstance(renderStyleData, list):
            renderStyleData = UISLineCreator.createStyledElement(renderStyleData, self._renderstyle)
        
        super().__init__(core, active, renderStyleData)


    @override
    def render(self, surface: UISurface) -> None:
        """
        render renders the UILine onto the given surface

        Args:
            surface: UISurface = the surface the UILine should be drawn on
        """
        assert self._drawer is not None

        rect: Rect = self._core.getBody().getRect()
        color: Optional[Color] = self._renderData.mainColor

        # check if UIElement should be rendered
        if not self._active:
            return

        if color is not None:
            self._drawer.drawline(surface, (rect.left, rect.top), (rect.right, rect.bottom), color)



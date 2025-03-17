from typing import Optional, override

from ...generic import Rect, Color
from ...uidrawerinterface import UISurface
from ...uirenderstyle import UIStyle

from ..uielementbody import UIABCBody
from ..uiline import UILine
from ..UIABC import UIABC
from .UIObjectCore import UIObjectCore
from .UISObject import UISObject
from .UISObjectCreateOptions import UISObjectCreateOptions
from .UIObjectRenderData import UIObjectRenderData
from .UISObjectCreator import UISObjectCreator
from .UISObjectPrefabs import UISObjectPrefabs


class UIObject(UIABC[UIObjectCore, UIObjectRenderData]):
    """
    UIObjectRender is the UIElementRender for all UIObjects.
    """

    def __init__(self, core: UIObjectCore | UIABCBody | Rect, active: bool=True, renderStyleData: UISObject | list[UISObjectCreateOptions] | UIObjectRenderData=UISObject.BASIC) -> None:
        """
        __init__ initializes the UIObjectRender instance

        Args:
            core: UIObject | UIABCBody | Rect = the refering UIObject (Or UIABCBody bcs. they are 'equivalet')
            active: bool = active-state of the UIObjectRenderer
            renderStyleElement: UIStyledTexts = the render style that should be used when rendering styled
        """
        assert self._renderstyle is not None

        if not isinstance(core, UIObjectCore):
            core = UIObjectCore(core)

        if isinstance(renderStyleData, UISObject):
            renderStyleData = UISObjectPrefabs.getPrefabRenderData(renderStyleData, self._renderstyle)
        elif isinstance(renderStyleData, list):
            renderStyleData = UISObjectCreator.createStyledElement(renderStyleData, self._renderstyle)
        
        super().__init__(core, active, renderStyleData)


    @override
    def render(self, surface: UISurface) -> None:
        """
        render renders the UIObject onto the given surface

        Args:
            surface: UISurface = the surface the UIObject should be drawn on
        """
        self.renderFill(surface)
        self.renderBorders(surface)

    def renderFill(self, surface: UISurface) -> None:
        
        assert self._drawer is not None

        rect: Rect = self._core.getBody().getRect()
        color: Optional[Color] = self._renderData.fillColor

        # check if UIElement should be rendered
        if not self._active:
            return


        if color is not None:
            self._drawer.drawrect(surface, rect, color)


    def renderBorders(self, surface: UISurface) -> None:
        
        assert self._drawer is not None

        rect: Rect = self._core.getBody().getRect()

        # check if UIElement should be rendered
        if not self._active:
            return

        if self._renderData.doBorders[0]:
            UILine(Rect((rect.left, rect.top), (rect.width, 0)), renderStyleData=self._renderData.borderData).render(surface)
        if self._renderData.doBorders[1]:
            UILine(Rect((rect.left, rect.top), (0, rect.height)), renderStyleData=self._renderData.borderData).render(surface)
        if self._renderData.doBorders[2]:
            UILine(Rect((rect.right, rect.top), (0, rect.height)), renderStyleData=self._renderData.borderData).render(surface)
        if self._renderData.doBorders[3]:
            UILine(Rect((rect.left, rect.bottom), (rect.width, 0)), renderStyleData=self._renderData.borderData).render(surface)


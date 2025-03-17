from typing import Optional, override

from ...generic import Rect, Color
from ...uidrawerinterface import UISurface
from ...uirenderstyle import UIStyle

from ..uielementbody import UIABCBody
from ..uiline import UILineRenderData
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
        if not isinstance(core, UIObjectCore):
            core = UIObjectCore(core)

        if isinstance(renderStyleData, UISObject):
            renderStyleData = UISObjectPrefabs.getPrefabRenderData(renderStyleData)
            print(f'im here: {renderStyleData}')
        elif isinstance(renderStyleData, list):
            renderStyleData = UISObjectCreator.createStyledObject(renderStyleData, UIStyle.MOON)
        
        super().__init__(core, active, renderStyleData)


    @override
    def render(self, surface: UISurface) -> None:
        """
        render renders the UIObject onto the given surface

        Args:
            surface: UISurface = the surface the UIObject should be drawn on
        """
        assert self._drawer is not None

        rect: Rect = self._core.getBody().getRect()
        fillColor: Optional[Color] = self._renderData.fillColor

        # check if UIElement should be rendered
        if not self._active:
            return


        if fillColor is not None:
            self._drawer.drawrect(surface, rect, fillColor)

        # !DEBUG!
        if self._renderData.borderData.mainColor is not None:
            if self._renderData.doBorders[0]:
                self._drawer.drawline(surface, (rect.left, rect.top), (rect.right, rect.top), self._renderData.borderData.mainColor)
            if self._renderData.doBorders[1]:
                self._drawer.drawline(surface, (rect.left, rect.top), (rect.left, rect.bottom), self._renderData.borderData.mainColor)
            if self._renderData.doBorders[2]:
                self._drawer.drawline(surface, (rect.right, rect.top), (rect.right, rect.bottom), self._renderData.borderData.mainColor)
            if self._renderData.doBorders[3]:
                self._drawer.drawline(surface, (rect.left, rect.bottom), (rect.right, rect.bottom), self._renderData.borderData.mainColor)

        
        # borders:
        # UISBorderRenderer(self._renderData.borderData).render(surfaceDrawer, surface, self._core.getBody().getRect())

        # TODO: ALT



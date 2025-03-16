from typing import override, Optional

from ...generic import Rect
from ...uidrawerinterface import UISurface

from ..uielementbody import UIABCBody
from ..uiline import UILineRenderData
from ..UIABC import UIABC
from .UIObjectCore import UIObjectCore
from .UISObject import UISObject
from .UISObjectCreateOptions import UISObjectCreateOptions
from .UIObjectRenderData import UIObjectRenderData


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
        if isinstance(renderStyleData, UIObjectRenderData):
            super().__init__(core, active, renderStyleData)
        else:
            super().__init__(core, active, UIObjectRenderData(UILineRenderData(), fillColor='white'))
            pass


    @override
    def render(self, surface: UISurface) -> None:
        """
        render renders the UIObject onto the given surface

        Args:
            surface: UISurface = the surface the UIObject should be drawn on
        """
        assert self._drawer is not None

        # check if UIElement should be rendered
        if not self._active:
            return


        if self._renderData.fillColor is not None:
            self._drawer.drawrect(surface, self._core.getBody().getRect(), self._renderData.fillColor)
        
        # borders:
        # UISBorderRenderer(self._renderData.borderData).render(surfaceDrawer, surface, self._core.getBody().getRect())

        # TODO: ALT



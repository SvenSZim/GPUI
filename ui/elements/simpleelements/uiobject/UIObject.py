from typing import Optional, override

from ...generic import Rect
from ...uidrawerinterface import UISurfaceDrawer, UISurface
from ...uirenderstyle import UIABCStyle, UIStyledObjects
from ..uielementbody import UIABCBody

from .UIABCObject import UIABCObject
from .UIABCObject import UIABCObjectRenderer


class UIObject(UIABCObject):
    """
    UIObject is a the most basic UI-Object
    It consists just of its body and a boolean which activates or deactivates itself
    """
    
    def __init__(self, body: UIABCBody | Rect) -> None:
        """
        __init__ initializes the UIObject instance

        Args:
            body: UIABCBody = the body of the UIObject
        """
        super().__init__(body)


class UIObjectRenderer(UIABCObjectRenderer[UIObject]):
    """
    UIObjectRender is the UIElementRender for all UIObjects.
    """

    def __init__(self, core: UIObject | UIABCBody | Rect, active: bool=True, renderStyleElement: Optional[UIStyledObjects]=None) -> None:
        """
        __init__ initializes the UIObjectRender instance

        Args:
            core: UIObject | UIABCBody | Rect = the refering UIObject (Or UIABCBody bcs. they are 'equivalet')
            active: bool = active-state of the UIObjectRenderer
            renderStyleElement: UIStyledTexts = the render style that should be used when rendering styled
        """
        if not isinstance(core, UIObject):
            core = UIObject(core)
        super().__init__(core, active, renderStyleElement)


    @override
    def render(self, surfaceDrawer: type[UISurfaceDrawer], surface: UISurface) -> None:
        """
        render renders the UIObject onto the given surface

        Args:
            surfaceDrawer: UISurfaceDrawer = the drawer to use when drawing on the surface
            surface: UISurface = the surface the UIObject should be drawn on
        """

        # check if UIElement should be rendered
        if not self._active:
            return

        surfaceDrawer.drawrect(surface, self._core.getRect(), 'white', fill=False)




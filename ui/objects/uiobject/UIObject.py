from typing import override

from ..idrawer import UISurfaceDrawer, UISurface
from ..uistyle import UIABCStyle, UIStyleObjects
from ..uiobjectbody import UIABCBody

from .UIABCObject import UIABCObject
from .UIABCObject import UIABCObjectRenderer


class UIObject(UIABCObject):
    """
    UIObject is a the most basic UI-Object
    It consists just of its body and a boolean which activates or deactivates itself
    """
    
    def __init__(self, body: UIABCBody) -> None:
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

    def __init__(self, core: UIObject | UIABCBody, active: bool=True) -> None:
        """
        __init__ initializes the UIObjectRender instance

        Args:
            core: UIObject | UIABCBody = the refering UIObject (Or UIABCBody bcs. they are 'equivalet')
            active: bool = active-state of the UIObjectRenderer
        """
        if isinstance(core, UIABCBody):
            core = UIObject(core)
        super().__init__(core, active)


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


    @override
    def renderStyled(self, surfaceDrawer: type[UISurfaceDrawer], surface: UISurface, renderStyle: type[UIABCStyle]) -> None:
        if not self._active:
            return
        
        if self._renderStyleElement is None:
            renderStyle.getStyledObject(UIStyleObjects.BASIC).render(surfaceDrawer, surface, self._core.getRect())
        else:
            renderStyle.getStyledObject(self._renderStyleElement).render(surfaceDrawer, surface, self._core.getRect())




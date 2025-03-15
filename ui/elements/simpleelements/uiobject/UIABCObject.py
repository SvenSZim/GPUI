from abc import ABC
from typing import Generic, TypeVar, override

from ...generic import Rect
from ...uidrawerinterface import UISurfaceDrawer, UISurface
from ...uirenderstyle import UIABCStyle, UIStyledObjects
from ..uielementbody import UIABCBody, UIStaticBody
from ..UIABC import UIABC
from ..UIABCRenderer import UIABCRenderer

class UIABCObject(UIABC[UIABCBody], ABC):
    """
    UIABCObject is the abstract base class for all UIObjects.
    """
    def __init__(self, body: UIABCBody | Rect) -> None:
        """
        __init__ initializes the values of UIABCObject for the UIObject

        Args:
            body: UIABCBody = the body value for the UIObject (for UIABC)
        """
        if isinstance(body, Rect):
            body = UIStaticBody(body)
        super().__init__(body)


Core = TypeVar('Core', bound=UIABCObject)

class UIABCObjectRenderer(Generic[Core], UIABCRenderer[Core, UIStyledObjects], ABC):
    """
    UIABCObjectRender is the abstract base class for all UIObjectRenderer.
    """
    def __init__(self, core: Core, active: bool=True) -> None:
        """
        __init__ initializes the values of UIABCObjectRenderer for the UIObjectRenderer

        Args:
            core: Core (bound=UIABCObject) = the refering UIObjectElement of the UIObjectRenderer (for UIABCRenderer)
            active: bool = active-state of the UIObjectRenderer (for UIABCRenderer)
        """
        super().__init__(core, active)

    @override
    def renderStyled(self, surfaceDrawer: type[UISurfaceDrawer], surface: UISurface, renderStyle: type[UIABCStyle]) -> None:
        if not self._active:
            return
        
        if self._renderStyleElement is None:
            renderStyle.getStyledObject(UIStyledObjects.BASIC).render(surfaceDrawer, surface, self._core.getRect())
        else:
            renderStyle.getStyledObject(self._renderStyleElement).render(surfaceDrawer, surface, self._core.getRect())



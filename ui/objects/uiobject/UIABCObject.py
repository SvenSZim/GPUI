from abc import ABC
from typing import Generic, TypeVar

from ..uiobjectbody import UIABCBody
from ..UIABC import UIABC
from ..UIABCRenderer import UIABCRenderer

class UIABCObject(UIABC[UIABCBody], ABC):
    """
    UIABCObject is the abstract base class for all UIObjects.
    """
    def __init__(self, body: UIABCBody) -> None:
        """
        __init__ initializes the values of UIABCObject for the UIObject

        Args:
            body: UIABCBody = the body value for the UIObject (for UIABC)
        """
        super().__init__(body)


Core = TypeVar('Core', bound=UIABCObject)

class UIABCObjectRenderer(Generic[Core], UIABCRenderer[Core], ABC):
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
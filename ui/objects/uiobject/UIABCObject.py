from abc import ABC
from typing import Generic, TypeVar

from ..UIABC import UIABC


class UIABCObject(UIABC, ABC):
    """
    UIABCObject is the abstract base class for all UIObjects.
    """
    pass


from ..UIABCRenderer import UIABCRenderer

B = TypeVar('B', bound=UIABCObject)

class UIABCObjectRenderer(Generic[B], UIABCRenderer[B], ABC):
    """
    UIABCObjectRender is the abstract base class for all UIObjectRenderer.
    """
    pass

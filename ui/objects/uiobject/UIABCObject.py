from abc import ABC
from dataclasses import dataclass
from typing import Generic, TypeVar

from ..UIABC import UIABC


class UIABCObject(UIABC, ABC):
    """
    UIABCObject is the abstract base class for all UIObjects.
    """
    pass


from ..UIABCRender import UIABCRenderInfo, UIABCRender

B = TypeVar('B', bound=UIABCObject)

@dataclass
class UIABCObjectRenderInfo(UIABCRenderInfo, ABC):
    """
    UIABCObjectRenderInfo is the abstract base class for all UIObjectRenderInfo.
    """
    active: bool = True # active status of rendering (activates or deactivates rendering)
    borders: tuple[bool, bool, bool, bool] | bool = True # draw borders

I = TypeVar('I', bound=UIABCObjectRenderInfo)

class UIABCObjectRender(Generic[B, I], UIABCRender[B, I], ABC):
    """
    UIABCObjectRender is the abstract base class for all UIObjectRender.
    """
    pass

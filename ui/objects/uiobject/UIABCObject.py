from abc import ABC
from dataclasses import dataclass
from typing import Generic, TypeVar

from ..UIABC import UIABC


class UIABCObject(UIABC, ABC):

    active: bool

    def getActive(self) -> bool:
        return self.active

    def toggleActive(self) -> bool:
        self.active = not self.active
        return self.active

    def setActive(self, active: bool) -> None:
        self.active = active




from ..UIABCRender import UIABCRenderInfo, UIABCRender

B = TypeVar('B', bound=UIABCObject)

@dataclass
class UIABCObjectRenderInfo(UIABCRenderInfo, ABC):
    borders: tuple[bool, bool, bool, bool] | bool = True

I = TypeVar('I', bound=UIABCObjectRenderInfo)

class UIABCObjectRender(Generic[B, I], UIABCRender[B, I], ABC):
    pass

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar

from .UIABC import UIABC

B = TypeVar('B', bound=UIABC)

@dataclass
class UIABCRenderInfo(ABC):
    pass

I = TypeVar('I', bound=UIABCRenderInfo)

class UIABCRender(Generic[B, I], ABC):
    
    body: B
    renderInfo: I

    def setRenderInfo(self, renderInfo: I) -> None:
        self.renderInfo = renderInfo

    def getUIObject(self) -> B:
        return self.body

    def getPosition(self) -> tuple[int, int]:
        return self.getUIObject().getPosition()

    def getSize(self) -> tuple[int, int]:
        return self.getUIObject().getSize()

    def getUIRenderInfo(self) -> I:
        return self.renderInfo

    def update(self) -> None:
        self.body.update()


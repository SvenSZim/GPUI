from abc import ABC
from typing import Generic, TypeVar

from .uiobjectbody import UIABCBody

B = TypeVar('B', bound=UIABCBody)


class UIABC(Generic[B], ABC):
    """
    UIABC is a abstract class to define functionality
    of UIObjects
    """

    body: B
    
    def getSize(self) -> tuple[int, int]:
        return (self.body.width, self.body.height)

    def getPosition(self) -> tuple[int, int]:
        return self.body.topleft

    def update(self) -> None:
        self.body.update()


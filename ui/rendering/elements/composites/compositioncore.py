from abc import ABC, abstractmethod

from ....utility    import Rect
from ..elementcore  import ElementCore

class CompositionCore(ElementCore, ABC):
    """
    CompositionCore is the abstract base class for all ui-atom-element-cores.
    """

    def __init__(self, rect: Rect) -> None:
        super().__init__(rect)

    @abstractmethod
    def getInnerSizing(self, elSize: tuple[int, int]) -> tuple[int, int]:
        pass

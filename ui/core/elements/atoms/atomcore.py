from abc import ABC, abstractmethod
from typing import Any, override

from ....utility  import Rect
from ..elementcore import ElementCore

class AtomCore(ElementCore, ABC):
    """
    AtomCore is the abstract base class for all ui-atom-element-cores.
    """

    # -------------------- creation --------------------

    def __init__(self, rect: Rect):
        super().__init__(rect)

    @abstractmethod
    def copy(self) -> 'AtomCore':
        pass

    # -------------------- getter --------------------

    @override
    def getInnerSizing(self, elSize: tuple[int, int], args: dict[str, Any]) -> tuple[int, int]:
        return elSize

    # -------------------- access-point --------------------

    @abstractmethod
    def set(self, args: dict[str, Any]) -> bool:
        pass
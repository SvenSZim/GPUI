from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from .....utility       import Rect
from ...element         import Element
from ..compositioncore  import CompositionCore

Inner = TypeVar('Inner', Element, list[Element])

class AddonCore(Generic[Inner], CompositionCore, ABC):
    
    _inner: Inner

    # -------------------- creation --------------------

    def __init__(self, outer: Rect, inner: Inner) -> None:
        super().__init__(outer)
        self._inner = inner
        self._alignInner()

    # -------------------- getter --------------------
    
    def getInner(self) -> Inner:
        return self._inner

    # -------------------- layout --------------------

    @abstractmethod
    def _alignInner(self) -> None:
        pass


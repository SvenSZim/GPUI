from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from .....utility       import Rect
from ...element         import Element
from ...elementcore     import ElementCore

Inner = TypeVar('Inner', Element, list[Element])

class AddonCore(Generic[Inner], ElementCore, ABC):
    """Core implementation for addon elements managing inner element behavior.
    
    Provides the base functionality for managing contained elements including:
    - Inner element storage and access
    - Layout alignment management
    - Z-index propagation
    - Active state control
    
    This class maintains the relationship between the addon wrapper
    and its contained elements while delegating specific behaviors
    to concrete implementations.
    """
    
    _inner: Inner

    # -------------------- creation --------------------

    def __init__(self, outer: Rect, inner: Inner) -> None:
        super().__init__(outer)
        self._inner = inner
        self._alignInner()

    # -------------------- getter --------------------
    
    def getInner(self) -> Inner:
        return self._inner

    # -------------------- setter --------------------

    @abstractmethod
    def setZIndex(self, zindex: int) -> None:
        pass

    # -------------------- layout --------------------

    @abstractmethod
    def _alignInner(self) -> None:
        pass

    # -------------------- active-state --------------------

    @abstractmethod
    def setActive(self, active: bool) -> None:
        pass


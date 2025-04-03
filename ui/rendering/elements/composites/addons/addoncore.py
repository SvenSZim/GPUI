from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Union, override

from .....utility   import Rect, iRect
from ...body        import LayoutManager
from ...element     import Element
from ...elementcore import ElementCore

Inner = TypeVar('Inner', bound=Union[Element, list[Element]])

class AddonCore(Generic[Inner], ElementCore, ABC):

    _inner: Inner

    def __init__(self, outer: Rect, inner: Inner) -> None:
        super().__init__(outer)
        self._inner = inner

    def getInner(self) -> Inner:
        return self._inner

    @abstractmethod
    def alignInner(self) -> None:
        pass
    
    @override
    def align(self, other: 'ElementCore | iRect', axis: int, offset: int=0, keepSize: bool=True) -> None:
        """
        align creates a LayoutRequest to align the axis of the core element with the given one.

        Args:
            other    (ElementCore or Rect)                       : the reference to align against
            axis     (int ~ 0: Left, 1: Right, 2: Top, 3: Bottom): the axis to align
            offset   (int)                                       : offset between the align
            keepSize (bool)                                      : boolean if the connection should keep the size
        """
        super().align(other, axis, offset, keepSize)
        self.alignInner()

    @override
    def alignnextto(self, other: 'ElementCore | iRect', where: int, offset: int=0, keepSize: bool=True) -> None:
        """
        alignnextto creates a LayoutRequest to align the core element next to a reference object.

        Args:
            other    (ElementCore or Rect)                              : the reference to align against
            where    (int ~ 0: to the Left, 1: Right, 2: Top, 3: Bottom): the position where to place the core
            offset   (int)                                              : offset between the align
            keepSize (bool)                                             : boolean if the connection should keep the size
        """
        super().alignnextto(other, where, offset, keepSize)
        self.alignInner()

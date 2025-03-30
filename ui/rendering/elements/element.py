from abc import ABC
from typing import Generic, TypeVar, override

from ..utility import Rect, iRect
from ..renderer import Renderer
from .core import ElementCore

Core = TypeVar('Core', bound=ElementCore) 

class Element(Generic[Core], Renderer, iRect, ABC):

    _core: Core     # refering UI-Element which gets rendered by the Renderer

    def __init__(self, core: Core, active: bool=True) -> None:
        super().__init__(active)
        self._core = core

    @override
    def getSize(self) -> tuple[int, int]:
        """
        getSize returns the size of the element.

        Returns (tuple[int, int]) ~ (width, height): size of the element
        """
        return self._core.getSize()

    @override
    def getPosition(self) -> tuple[int, int]:
        """
        getPosition return the position of the element.

        Returns (tuple[int, int]) ~ (x-pos, y-pos): position of the element
        """
        return self._core.getPosition()

    def getRect(self) -> Rect:
        """
        getRect returns the position and size of the element stored in a Rect object

        Returns (Rect): Rect object containing the pos and size of the element
        """
        return self._core.getRect()

    def getCore(self) -> Core:
        """
        getCore returns the stored core of the element.
        (should only be used to align)

        Returns (Core): the stored core of the element
        """
        return self._core
    
    def align(self, other: 'Element | Core | iRect', axis: int, keepSize: bool=True) -> None:
        """
        align creates a LayoutRequest to align the axis of the core element with the given one.

        Args:
            other (ElementCore or Rect)                       : the reference to align against
            axis  (int ~ 0: Left, 1: Right, 2: Top, 3: Bottom): the axis to align
        """
        if isinstance(other, Element):
            other = other.getCore()
        self._core.align(other, axis, keepSize)

    def alignnextto(self, other: 'Element | Core | iRect', where: int, keepSize: bool=True) -> None:
        """
        alignnextto creates a LayoutRequest to align the core element next to a reference object.

        Args:
            other (ElementCore or Rect)                              : the reference to align against
            where (int ~ 0: to the Left, 1: Right, 2: Top, 3: Bottom): the position where to place the core
        """
        if isinstance(other, Element):
            other = other.getCore()
        self._core.alignnextto(other, where, keepSize)

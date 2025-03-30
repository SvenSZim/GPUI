from abc import ABC
from typing import override

from ...utility import Rect, iRect
from .body import Body, BodyManager, LayoutManager

class ElementCore(iRect, ABC):
    """
    ElementCore is a abstract base class for all ui element cores.
    Cores are used to store meta-info about ui-elements which is not just
    about rendering (like content for text elements or the position on the screen).
    ElementCore has some basic functionality to position elements on the screen.
    """

    _body: Body

    def __init__(self, rect: Rect) -> None:
        self._body = BodyManager.createBody()
        self._body.setRect(rect)

    @override
    def getSize(self) -> tuple[int, int]:
        """
        getSize returns the size of the element.

        Returns (tuple[int, int]) ~ (width, height): size of the element
        """
        return self._body.getSize()

    @override
    def getPosition(self) -> tuple[int, int]:
        """
        getPosition return the position of the element.

        Returns (tuple[int, int]) ~ (x-pos, y-pos): position of the element
        """
        return self._body.getPosition()

    def getRect(self) -> Rect:
        """
        getRect returns the position and size of the element stored in a Rect object

        Returns (Rect): Rect object containing the pos and size of the element
        """
        return self._body.getRect()

    def getBody(self) -> Body:
        """
        getBody returns the stored body element.
        (should only be used to create connections between cores)

        Returns (Body): the stored body element
        """
        return self._body

    def align(self, other: 'ElementCore | iRect', axis: int, offset: int=0, keepSize: bool=True) -> None:
        """
        align creates a LayoutRequest to align the axis of the core element with the given one.

        Args:
            other    (ElementCore or Rect)                       : the reference to align against
            axis     (int ~ 0: Left, 1: Right, 2: Top, 3: Bottom): the axis to align
            offset   (int)                                       : offset between the align
            keepSize (bool)                                      : boolean if the connection should keep the size
        """
        if isinstance(other, ElementCore):
            other = other.getBody()
        match axis:
            case 0:
                LayoutManager.addConnection((True, False), self._body, other, (0.0, 0.0), (0.0, 0.0), offset=offset, keepSizeFix=keepSize)
            case 1:
                LayoutManager.addConnection((True, False), self._body, other, (1.0, 0.0), (1.0, 0.0), offset=offset, keepSizeFix=keepSize)
            case 2:
                LayoutManager.addConnection((False, True), self._body, other, (0.0, 0.0), (0.0, 0.0), offset=offset, keepSizeFix=keepSize)
            case 3:
                LayoutManager.addConnection((False, True), self._body, other, (0.0, 1.0), (0.0, 1.0), offset=offset, keepSizeFix=keepSize)

    def alignnextto(self, other: 'ElementCore | iRect', where: int, offset: int=0, keepSize: bool=True) -> None:
        """
        alignnextto creates a LayoutRequest to align the core element next to a reference object.

        Args:
            other    (ElementCore or Rect)                              : the reference to align against
            where    (int ~ 0: to the Left, 1: Right, 2: Top, 3: Bottom): the position where to place the core
            offset   (int)                                              : offset between the align
            keepSize (bool)                                             : boolean if the connection should keep the size
        """
        if isinstance(other, ElementCore):
            other = other.getBody()
        match where:
            case 0:
                LayoutManager.addConnection((True, False), self._body, other, (1.0, 0.0), (0.0, 0.0), offset=offset, keepSizeFix=keepSize)
            case 1:
                LayoutManager.addConnection((True, False), self._body, other, (0.0, 0.0), (1.0, 0.0), offset=offset, keepSizeFix=keepSize)
            case 2:
                LayoutManager.addConnection((False, True), self._body, other, (0.0, 1.0), (0.0, 0.0), offset=offset, keepSizeFix=keepSize)
            case 3:
                LayoutManager.addConnection((False, True), self._body, other, (0.0, 0.0), (0.0, 1.0), offset=offset, keepSizeFix=keepSize)

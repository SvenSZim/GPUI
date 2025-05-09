from abc import ABC
from typing import override

from ...utility import Rect, iRect
from .body      import Body

Point = tuple[float, float]

class ElementCore(iRect, ABC):
    """
    ElementCore is a abstract base class for all ui element cores.
    Cores are used to store meta-info about ui-elements which is not just
    about rendering (like content for text elements or the position on the screen).
    ElementCore has some basic functionality to position elements on the screen.
    """

    _body: Body

    # -------------------- creation --------------------

    def __init__(self, rect: Rect) -> None:
        self._body = Body(rect)

    # -------------------- iRect-implementation --------------------

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

    # -------------------- additional-getter --------------------

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

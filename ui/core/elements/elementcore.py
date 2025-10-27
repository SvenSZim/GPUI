from abc import ABC, abstractmethod
from typing import Any, override

from ...utility import Rect, iRect
from .body      import Body

Point = tuple[float, float]

class ElementCore(iRect, ABC):
    """ElementCore

    Abstract base for UI element cores.

    Cores store non-render-specific metadata and layout-related
    functionality for UI elements (for example content, logical
    position, and connections used by the layout engine).

    Subclasses must implement getInnerSizing to calculate inner content
    sizing behavior.
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

    @abstractmethod
    def getInnerSizing(self, elSize: tuple[int, int], args: dict[str, Any]) -> tuple[int, int]:
        pass

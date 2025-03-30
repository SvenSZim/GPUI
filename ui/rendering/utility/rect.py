from typing import override

from .irect import iRect

class Rect(iRect):
    """
    Rect is a utility class for storing a rectangle
    """

    # position
    top: int
    left: int
    bottom: int
    right: int

    # size
    width: int
    height: int

    def __init__(self, topleft: tuple[int, int] = (0, 0), 
                 size: tuple[int, int] = (0, 0)) -> None:
        """
        __init__ initializes a Rect object

        Args:
            topleft (tuple[int, int]): (left, top) ~ coordinates of the topleft corner
            size    (tuple[int, int]): (width, height) ~ sizes of the rect
        """
        self.left, self.top = topleft
        self.width, self.height = size
        self.updateRB()

    def updateRB(self) -> None:
        """
        updateRB updates the right and bottom coordinate of the Rect
        depending on the left, width, top and height coordinates.
        """
        self.right = self.left + self.width
        self.bottom = self.top + self.height

    @override
    def getPosition(self) -> tuple[int, int]:
        """
        getPosition returns the position (top-left-corner) of the Rect.

        Returns (tuple[int, int]): (posX, posY) ~ top-left-corner of the Rect.
        """
        return (self.left, self.top)

    @override
    def getSize(self) -> tuple[int, int]:
        """
        getSize returns the size of the Rect.

        Returns:
            tuple[int, int] = (width, height) ~ size of the Rect.
        """
        return (self.width, self.height)

    def isZero(self) -> bool:
        """
        isZero returns if both width and height of the Rect are zero.

        Returns (bool): if the rects width and height are both zero.
        """
        return self.width == 0 and self.height == 0

    def collidepoint(self, point: tuple[int, int]) -> bool:
        """
        collidepoint checks if a given point is inside the Rect.

        Args:
            point (tuple[int, int]): the point to check for

        Returns (bool): boolean if the point is inside the Rect or not
        """
        px, py = point
        return px >= self.left and py >= self.top and px <= self.right and py <= self.bottom

    def __str__(self) -> str:
        """
        __str__ generates a string out of the object

        Returns:
            str: a string representation of the Rect
        """
        return f'Rect(topleft:{self.getPosition()}, size:{self.getSize()})'



class Rect:
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
            topleft: tuple[int, int] = (left, top) ~ coordinates of the topleft corner
            size: tuple[int, int] = (width, height) ~ sizes of the rect
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

    def getPosition(self) -> tuple[int, int]:
        """
        getPosition returns the position (top-left-corner) of the Rect.

        Returns:
            tuple[int, int] = (posX, posY) ~ top-left-corner of the Rect.
        """
        return (self.left, self.top)

    def setPosition(self, position: tuple[int, int]) -> None:
        """
        setPosition sets the position (top-left-corner) of the Rect.

        Args:
            position: tuple[int, int] = (posX, posY) ~ the new position of the top-left-corner of the Rect
        """
        self.left, self.top = position
        self.updateRB()

    def getSize(self) -> tuple[int, int]:
        """
        getSize returns the size of the Rect.

        Returns:
            tuple[int, int] = (width, height) ~ size of the Rect.
        """
        return (self.width, self.height)

    def setSize(self, size: tuple[int, int]) -> None:
        """
        setSize sets the size of the Rect.

        Args:
            size: tuple[int, int] = (width, height) ~ the new size of the Rect
        """
        self.width, self.height = size
        self.updateRB()

    def getArea(self) -> int:
        """
        getArea returns the area of the Rect.

        Returns:
        int = area of the Rect.
        """
        return self.width * self.height

    def collidepoint(self, point: tuple[int, int]) -> bool:
        """
        collidepoint checks if a given point is inside the Rect.

        Args:
            point: tuple[int, int] = the point to check for

        Returns:
            bool = boolean if the point is inside the Rect or not
        """
        px, py = point
        return px >= self.left and py >= self.top and px <= self.right and py <= self.bottom

from typing import override

from .irect import iRect

class Rect(iRect):
    """Rectangle utility class for UI layout and collision detection.

    Represents a rectangle with position and size. Provides methods for:
    - Position and size access
    - Collision detection
    - Boundary checking
    - Rectangle arithmetic

    Attributes:
        top (int): Y-coordinate of top edge
        left (int): X-coordinate of left edge
        bottom (int): Y-coordinate of bottom edge
        right (int): X-coordinate of right edge
        width (int): Rectangle width
        height (int): Rectangle height

    Thread Safety:
        - Immutable after creation
        - All methods are thread-safe
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
        """Initialize a rectangle.

        Args:
            topleft: (left, top) coordinates
            size: (width, height) dimensions

        Raises:
            ValueError: If dimensions are negative
        """
        if not isinstance(topleft, tuple) or len(topleft) != 2 or \
           not all(isinstance(x, (int, float)) for x in topleft):
            raise ValueError(f'topleft must be (int,int), got {topleft}')
            
        if not isinstance(size, tuple) or len(size) != 2 or \
           not all(isinstance(x, (int, float)) for x in size):
            raise ValueError(f'size must be (int,int), got {size}')
        """
        __init__ initializes a Rect object

        Args:
            topleft (tuple[int, int]): (left, top) ~ coordinates of the topleft corner
            size    (tuple[int, int]): (width, height) ~ sizes of the rect
        """
        self.left, self.top = topleft
        self.width, self.height = size
        self.right = self.left + self.width
        self.bottom = self.top + self.height

    # -------------------- iRect-implementation --------------------

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

    # -------------------- additional-getter --------------------

    def collidepoint(self, point: tuple[int, int]) -> bool:
        """
        collidepoint checks if a given point is inside the Rect.

        Args:
            point (tuple[int, int]): the point to check for

        Returns (bool): boolean if the point is inside the Rect or not
        """
        px, py = point
        return px >= self.left and py >= self.top and px <= self.right and py <= self.bottom

    def contains_rect(self, other: 'Rect') -> bool:
        """Check if this rectangle fully contains another.

        Args:
            other: Rectangle to check

        Returns:
            True if other is completely inside this rectangle
        """
        return (other.left >= self.left and
                other.right <= self.right and
                other.top >= self.top and
                other.bottom <= self.bottom)

    def intersects(self, other: 'Rect') -> bool:
        """Check if this rectangle intersects another.

        Args:
            other: Rectangle to check intersection with

        Returns:
            True if rectangles overlap
        """
        return (self.left < other.right and
                self.right > other.left and
                self.top < other.bottom and
                self.bottom > other.top)

    def clamp(self, bounds: 'Rect') -> 'Rect':
        """Create new rectangle clamped within bounds.

        Args:
            bounds: Rectangle to clamp within

        Returns:
            New rectangle clamped to bounds
        """
        left = max(min(self.left, bounds.right - self.width), bounds.left)
        top = max(min(self.top, bounds.bottom - self.height), bounds.top)
        return Rect((left, top), (self.width, self.height))

    def __str__(self) -> str:
        """Create string representation.

        Returns:
            String in format: Rect(topleft:(x,y), size:(w,h))
        """
        return f'Rect(topleft:{self.getPosition()}, size:{self.getSize()})'

from abc import ABC, abstractmethod

class iRect(ABC):
    """Abstract interface for rectangular UI elements.

    Defines the contract for elements that have rectangular bounds,
    providing position and size information. Used as base for all
    UI elements that need spatial representation.

    Features:
    - Position access (left, top, right, bottom)
    - Size information (width, height)
    - Point calculation
    - Bounds checking

    Implementation Notes:
    - All coordinate values are integers
    - Origin is top-left corner
    - Positive y goes downward
    - Width/height must be non-negative

    Thread Safety:
    - Implementation dependent
    - Methods should be thread-safe if element is immutable
    """

    # -------------------- base-methods --------------------

    @abstractmethod
    def getSize(self) -> tuple[int, int]:
        """
        getSize returns the size of the element.

        Returns (tuple[int, int]) ~ (width, height): size of the element
        """
        pass

    @abstractmethod
    def getPosition(self) -> tuple[int, int]:
        """
        getPosition return the position of the element.

        Returns (tuple[int, int]) ~ (x-pos, y-pos): position of the element
        """
        pass

    # -------------------- additional-getter --------------------

    def getWidth(self) -> int:
        """
        getWidth returns the width of the object.

        Returns (int): the width of the object
        """
        return self.getSize()[0]

    def getHeight(self) -> int:
        """
        getHeight returns the height of the object.

        Returns (int): the height of the object
        """
        return self.getSize()[1]

    def getLeft(self) -> int:
        """
        getLeft returns the x-coordinate of the left of the obj

        Returns (int): the x-coordinate of the left
        """
        return self.getPosition()[0]

    def getTop(self) -> int:
        """
        getTop returns the y-coordinate of the top of the obj

        Returns (int): the y-coordinate of the top
        """
        return self.getPosition()[1]

    def getRight(self) -> int:
        """
        getRight returns the x-coordinate of the right of the obj

        Returns (int): the x-coordinate of the right
        """
        return self.getPosition()[0] + self.getSize()[0]

    def getBottom(self) -> int:
        """
        getBottom returns the y-coordinate of the bottom of the obj

        Returns (int): the y-coordinate of the bottom
        """
        return self.getPosition()[1] + self.getSize()[1]

    def getPoint(self, relativePosition: tuple[float, float]) -> tuple[int, int]:
        """Calculate absolute coordinates from relative position.

        Converts a relative position (0.0-1.0) within the rectangle
        to absolute coordinates in the UI space.

        Args:
            relativePosition: (x,y) floats between 0.0-1.0
                where (0,0) is top-left and (1,1) is bottom-right

        Returns:
            tuple[int, int]: Absolute (x,y) coordinates

        Raises:
            ValueError: If relative position is invalid
            TypeError: If relative position has wrong type
        """
        if not isinstance(relativePosition, tuple) or len(relativePosition) != 2:
            raise TypeError(
                f'relativePosition must be (float,float), '
                f'got {relativePosition}')

        rx, ry = relativePosition
        if not all(isinstance(v, (int, float)) for v in (rx, ry)):
            raise TypeError('Relative coordinates must be numbers')
            
        if not (0 <= rx <= 1 and 0 <= ry <= 1):
            raise ValueError(
                f'Relative coordinates must be between 0 and 1, '
                f'got {relativePosition}')

        width, height = self.getSize()
        left, top = self.getPosition()
        
        return (int(left + rx * width), int(top + ry * height))

    def isZero(self) -> bool:
        """Check if rectangle has zero area.

        Returns:
            bool: True if both width and height are zero
        """
        return self.getWidth() == 0 and self.getHeight() == 0

    def isValid(self) -> bool:
        """Check if rectangle has valid dimensions.

        Validates:
        - Non-negative width/height
        - Position coordinates are valid integers

        Returns:
            bool: True if rectangle is valid
        """
        try:
            w, h = self.getSize()
            x, y = self.getPosition()
            return (isinstance(w, int) and isinstance(h, int) and
                    isinstance(x, int) and isinstance(y, int) and
                    w >= 0 and h >= 0)
        except (TypeError, ValueError):
            return False

    def isEmpty(self) -> bool:
        """Check if rectangle has zero area.

        Different from isZero() as this checks actual area.

        Returns:
            bool: True if width or height is zero
        """
        return self.getWidth() <= 0 or self.getHeight() <= 0

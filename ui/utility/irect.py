from abc import ABC, abstractmethod

class iRect(ABC):
    """
    iRect is a abstract class to specify behavior of rect-elements
    (elements that contain positional and sizing information similar to rectangles)
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
        """
        getPoint returns the absolute coordinate of a relative position inside the object.

        Args:
            relativePosition (tuple[float, float]): the relative position inside the object

        Returns (tuple[int, int]): the absolute position in world-space
        """
        width, height = self.getSize()
        left, top = self.getPosition()
        return (int(left + relativePosition[0] * width), int(top + relativePosition[1] * height))

    def isZero(self) -> bool:
        """
        isZero returns if both width and height of the Rect are zero.

        Returns (bool): if the rects width and height are both zero.
        """
        return self.getWidth() == 0 and self.getHeight() == 0

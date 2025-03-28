from abc import ABC, abstractmethod

from ...generic import Rect

class UIABCBody(ABC):
    """
    UIABCBody is the abstract base class for all UIElementBodys.
    It defines the needed functionality all UIElementBodys should implement.
    """

    @abstractmethod
    def getRect(self) -> Rect:
        """
        getRect returns the cached Rect of the UIElementBody

        Returns:
            Rect = the cached Rect of the UIElementBody
        """
        pass

    def getPosition(self) -> tuple[int, int]:
        """
        getPosition returns the cached position (top-left-corner) of the UIElementBody

        Returns:
            tuple[int, int] = (posX, posY) ~ the position of the top-left-corner of the UIElementBody
        """
        return self.getRect().getPosition()

    def getSize(self) -> tuple[int, int]:
        """
        getSize returns the cached size of the UIElementBody

        Returns:
            tuple[int, int] = (width, height) ~ the size of the UIElementBody
        """
        return self.getRect().getSize()
    
    @abstractmethod
    def update(self) -> None:
        """
        update calculates the position and size of the UIElementBody and
        caches the values in the UIElementBody attributes.
        """
        pass

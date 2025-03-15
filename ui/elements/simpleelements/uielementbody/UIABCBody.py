from abc import ABC, abstractmethod

from ...generic import Rect

class UIABCBody(ABC):
    """
    UIABCBody is the abstract base class for all UIElementBodys.
    It defines the needed functionality all UIElementBodys should implement.
    """

    _rect: Rect # cached object data

    def __init__(self, rect: Rect) -> None:
        """
        __init__ initializes the values of UIABCBody for the UIBodyElement

        Args:
            rect: Rect = the rect containing the start position and sizing of the UIBodyElement
        """
        self._rect = rect

    def getRect(self) -> Rect:
        """
        getRect returns the cached Rect of the UIElementBody

        Returns:
            Rect = the cached Rect of the UIElementBody
        """
        return self._rect

    def getPosition(self) -> tuple[int, int]:
        """
        getPosition returns the cached position (top-left-corner) of the UIElementBody

        Returns:
            tuple[int, int] = (posX, posY) ~ the position of the top-left-corner of the UIElementBody
        """
        return self._rect.getPosition()

    def getSize(self) -> tuple[int, int]:
        """
        getSize returns the cached size of the UIElementBody

        Returns:
            tuple[int, int] = (width, height) ~ the size of the UIElementBody
        """
        return self._rect.getSize()
    
    @abstractmethod
    def update(self) -> None:
        """
        update calculates the position and size of the UIElementBody and
        caches the values in the UIElementBody attributes.
        """
        pass

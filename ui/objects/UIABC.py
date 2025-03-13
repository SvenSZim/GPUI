from abc import ABC
from typing import Generic, TypeVar

from .generic import Rect
from .uiobjectbody import UIABCBody

B = TypeVar('B', bound=UIABCBody)


class UIABC(Generic[B], ABC):
    """
    UIABC is the abstract base class for all UIElements.
    """

    body: B # A UIBody which contains the positioning of the UIElement

    def getRect(self) -> Rect:
        """
        getRect returns the rect of the UIElement

        Returns:
            Rect = rect of the UIElement
        """
        return self.body.getRect()
    
    def getSize(self) -> tuple[int, int]:
        """
        getSize returns the size of the UIElement

        Returns:
            tuple[int, int]: width, height of UIElement
        """
        return self.getRect().getSize()

    def getPosition(self) -> tuple[int, int]:
        """
        getPosition returns the position (top-left-corner) of the UIElement

        Returns:
            tuple[int, int]: posX, posY of the UIElement
        """
        return self.getRect().getPosition()

    def update(self) -> None:
        """
        update updates the position and sizing of the UIElement
        """
        self.body.update()


from abc import ABC
from typing import Generic, TypeVar

from .generic import Rect
from .uiobjectbody import UIABCBody

Body = TypeVar('Body', bound=UIABCBody)


class UIABC(Generic[Body], ABC):
    """
    UIABC is the abstract base class for all UIElements.
    """

    _body: Body # A UIBody which contains the positioning of the UIElement

    def __init__(self, body: Body):
        """
        __init__ initializes the values of UIABC for the UIElement

        Args:
            body: Body (bound=UIABCBody) = the body value for the UIElement
        """
        self._body = body
        self.update()

    def getBody(self) -> Body:
        """
        getBody returns the body of the UIElements
        (should only be used to create references between the objects like in DynamicBody!)

        Returns:
            Body = the body of the UIElement
        """
        return self._body

    def getRect(self) -> Rect:
        """
        getRect returns the rect of the UIElement

        Returns:
            Rect = rect of the UIElement
        """
        return self._body.getRect()
    
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
        self._body.update()


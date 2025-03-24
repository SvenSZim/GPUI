from typing import Optional, override

from ...generic import Rect
from .UIABCBody import UIABCBody

class UIStaticBody(UIABCBody):
    """
    UIStaticBody is a basic implementation of UIABCBody where the
    position and the size of the object are fixed.
    """

    __rect: Rect

    def __init__(self, positionORrect: tuple[int, int] | Rect, size: Optional[tuple[int, int]]=None) -> None:
        """
        __init__ initializes the UIStaticBody with either a rect or the position and size of the rect.

        Args:
            Option1:
            position: tuple[int, int] = (left, top) ~ top left corner as absolute position of the object
            size: tuple[int, int] = (width, height) ~ the size of the object
            Option2:
            rect: Rect = the position and size of the object as rect
        """
        if isinstance(positionORrect, Rect):
            self.__rect = positionORrect
        elif size is None:
            raise ValueError("UIStaticBody::__init__::incomplete initialization arguments!")
        else:
            self.__rect = Rect(positionORrect, size)

    @override
    def getRect(self) -> Rect:
        return self.__rect

    @override
    def update(self) -> None:
        pass

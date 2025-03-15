from abc import ABC, abstractmethod
from typing import Optional, Union

from ....generic import Rect, Color
from ..UIABCStyledElement import UIABCStyledElement


class UIABCStyledObject(UIABCStyledElement[Rect], ABC):
    """
    UIABCStyleObject is the abstract base class for all UIStyleObjects
    """
    _drawBorder: tuple[bool, bool, bool, bool]
    _borderColor: Optional[Union[str, tuple[int, int, int], Color]]
    _fillColor: Optional[Union[str, tuple[int, int, int], Color]]
    
    def __init__(self, drawBorder: tuple[bool, bool, bool, bool]=(False, False, False, False),
                 borderColor: Optional[Union[str, tuple[int, int, int], Color]]=None,
                 fillColor: Optional[Union[str, tuple[int, int, int], Color]]=None) -> None:
        self._drawBorder = drawBorder
        self._borderColor = borderColor
        self._fillColor = fillColor

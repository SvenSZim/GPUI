from abc import ABC

from ....generic import Rect
from ..UIABCStyledElement import UIABCStyledElement


class UIABCStyledObject(UIABCStyledElement[Rect], ABC):
    """
    UIABCStyleObject is the abstract base class for all UIStyleObjects
    """

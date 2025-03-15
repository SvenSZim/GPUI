from abc import ABC

from ....generic import Rect
from ..UIABCStyledElement import UIABCStyledElement


class UIABCStyledButton(UIABCStyledElement[tuple[Rect, int, int]], ABC):
    """
    UIABCStyleButton is the abstract base class for all UIStyleButtons
    """

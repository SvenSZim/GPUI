from abc import ABC
from typing import Union

from ....generic import Rect, Color
from ....uidrawerinterface import UIFont
from ..UIABCStyledElement import UIABCStyledElement


class UIABCStyledText(UIABCStyledElement[tuple[Rect, str, UIFont, Union[str, tuple[int, int, int], Color]]], ABC):
    """
    UIABCStyleText is the abstract base class for all UIStyleText
    """

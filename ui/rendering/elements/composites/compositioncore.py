from abc import ABC

from ....utility    import Rect
from ..elementcore  import ElementCore

class CompositionCore(ElementCore, ABC):
    """
    CompositionCore is the abstract base class for all ui-atom-element-cores.
    """

    def __init__(self, rect: Rect) -> None:
        super().__init__(rect)

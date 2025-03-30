
from ....utility import Rect
from ..atomcore import AtomCore

class BoxCore(AtomCore):
    """
    BoxCore is the core object of the atom-element 'Box'.
    """
    def __init__(self, rect: Rect) -> None:
        super().__init__(rect)

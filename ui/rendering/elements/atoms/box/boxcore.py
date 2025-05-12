from typing import override

from .....utility import Rect
from ..atomcore import AtomCore

class BoxCore(AtomCore):
    """
    BoxCore is the core object of the atom-element 'Box'.
    """
    
    # -------------------- creation --------------------

    def __init__(self, rect: Rect) -> None:
        super().__init__(rect)

    @override
    def copy(self) -> 'BoxCore':
        return BoxCore(Rect())

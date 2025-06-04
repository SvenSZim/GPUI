from typing import Any, override

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

    # -------------------- access-point --------------------

    @override
    def set(self, args: dict[str, Any]) -> bool:
        return False
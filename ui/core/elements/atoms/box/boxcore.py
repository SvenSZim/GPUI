from typing import Any, override

from .....utility import Rect
from ..atomcore import AtomCore

class BoxCore(AtomCore):
    """
    BoxCore is the core object of the atom-element 'Box'.
    """
    
    # -------------------- creation --------------------

    def __init__(self) -> None:
        super().__init__(Rect())

    @override
    def copy(self) -> 'BoxCore':
        return BoxCore()

    # -------------------- access-point --------------------

    @override
    def set(self, args: dict[str, Any], skips: bool) -> bool:
        return False

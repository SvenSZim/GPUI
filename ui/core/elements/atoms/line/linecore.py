from typing import Any, override

from .....utility import Rect
from ..atomcore import AtomCore

class LineCore(AtomCore):
    """
    LineCore is the core object of the atom-element 'Line'.
    """
    def __init__(self) -> None:
        super().__init__(Rect())

    @override
    def copy(self) -> 'LineCore':
        return LineCore()

    # -------------------- access-point --------------------

    @override
    def set(self, args: dict[str, Any], skips: bool) -> bool:
        return False

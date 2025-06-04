from typing import Any, override

from .....utility import Rect
from ..atomcore import AtomCore

class LineCore(AtomCore):
    """
    LineCore is the core object of the atom-element 'Line'.
    """
    def __init__(self, rect: Rect) -> None:
        super().__init__(rect)

    def copy(self) -> 'LineCore':
        return LineCore(Rect())

    # -------------------- access-point --------------------

    @override
    def set(self, args: dict[str, Any]) -> bool:
        return False

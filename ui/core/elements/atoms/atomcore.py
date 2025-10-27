from abc import ABC, abstractmethod
from typing import Any, override

from ....utility  import Rect
from ..elementcore import ElementCore

class AtomCore(ElementCore, ABC):
    """Abstract base class for atomic UI element cores.

    Provides core functionality for atomic elements including:
    - Rectangle bounds management
    - Size calculations
    - Property access
    - State management

    The core handles structural aspects while leaving visual
    properties to AtomData.

    Implementation Requirements:
    - Must implement copy() for cloning
    - Must implement set() for property updates
    - Should maintain valid rectangle bounds
    - Should validate size calculations

    Thread Safety:
    - Rectangle access is synchronized
    - Property updates are atomic
    - Size calculations are thread-safe
    """

    def __init__(self, rect: Rect):
        """Initialize atom core with bounds.

        Args:
            rect: Initial bounding rectangle

        Raises:
            TypeError: If rect is not a Rect instance
            ValueError: If rect is invalid
        """
        if not isinstance(rect, Rect):
            raise TypeError(f'rect must be Rect instance, got {type(rect)}')
        if not rect.isValid():
            raise ValueError(f'Invalid rectangle: {rect}')

        super().__init__(rect)

    @abstractmethod
    def copy(self) -> 'AtomCore':
        pass

    # -------------------- getter --------------------

    @override
    def getInnerSizing(self, elSize: tuple[int, int], args: dict[str, Any]) -> tuple[int, int]:
        return elSize

    # -------------------- access-point --------------------

    @abstractmethod
    def set(self, args: dict[str, Any], skips: bool) -> bool:
        pass

from abc import ABC, abstractmethod
from typing import Any, Generic, override, TypeVar

from ..element         import Element
from .atomcore         import AtomCore
from .atomdata         import AtomData

Core         = TypeVar('Core'        , bound=AtomCore)
RenderData   = TypeVar('RenderData'  , bound=AtomData)

class Atom(Generic[Core, RenderData], Element[Core, RenderData], ABC):
    """Abstract base class for atomic UI elements.

    Atoms are the most basic building blocks of the UI system that cannot
    be broken down further. They implement core rendering and behavior.

    Type Parameters:
        Core: AtomCore subclass defining element structure
        RenderData: AtomData subclass for render properties

    Features:
        - Atomic rendering (no child elements)
        - Self-contained state
        - Direct property access
        - Automatic render updates

    Thread Safety:
        - Core data access is synchronized
        - Render updates are atomic
        - Property access is thread-safe
    """

    def __init__(self, core: Core, renderData: RenderData, active: bool) -> None:
        """Initialize atomic UI element.

        Args:
            core: Element core structure
            renderData: Render properties
            active: Initial active state

        Raises:
            TypeError: If core or renderData have invalid types
            ValueError: If core or renderData are invalid
        """
        if not isinstance(core, AtomCore):
            raise TypeError(f'core must be AtomCore, got {type(core)}')
        if not isinstance(renderData, AtomData):
            raise TypeError(f'renderData must be AtomData, got {type(renderData)}')

        super().__init__(core, renderData, active)

    @abstractmethod
    def copy(self) -> 'Atom':
        pass

    # -------------------- access-point --------------------

    @override
    def _set(self, args: dict[str, Any], sets: int = -1, maxDepth: int = -1, skips: bool=False) -> bool:
        s: bool = super()._set(args, sets, maxDepth, skips)
        s |= self._core.set(args, skips)
        s |= self._renderData.set(args, skips)
        if s:
            self.updateRenderData()
        return s

    @override
    def set(self, args: dict[str, Any], sets: int = -1, maxDepth: int = -1, skips: list[int]=[0]) -> int:
        """Update element properties from argument dictionary.

        General access point for updating element properties. Handles:
        1. Core property updates
        2. Render data updates
        3. Element-specific behavior

        Args:
            args: Property name/value pairs to apply
            sets: Max number of successful updates (-1 for unlimited)
            maxDepth: Max recursion depth (-1 for unlimited)
            skips: Number of matches to skip [0] (for partial updates)

        Returns:
            int: Number of successful property updates

        Raises:
            TypeError: If args is not a dictionary
            ValueError: If args contains invalid values
            
        Note:
            Uses validateRequiredArgs from Parsable for validation
        """
        # Validate input
        if not isinstance(args, dict):
            raise TypeError(f'args must be a dictionary, got {type(args)}')
        if not isinstance(sets, int):
            raise TypeError(f'sets must be an integer, got {type(sets)}')
        if not isinstance(maxDepth, int):
            raise TypeError(f'maxDepth must be an integer, got {type(maxDepth)}')
        if not isinstance(skips, list) or not all(isinstance(x, int) for x in skips):
            raise TypeError('skips must be a list of integers')
        s: bool = self._set(args, sets, maxDepth, bool(skips[0]))
        if s and skips[0]:
            skips[0] -= 1
            return 0
        return int(s)

    # -------------------- rendering --------------------

    @override
    def forceUpdate(self) -> None:
        super().forceUpdate()
        self.updateRenderData()

    @abstractmethod
    def updateRenderData(self) -> None:
        """Update render data from current state.

        This method should be called whenever the element's state changes
        and render data needs to be recalculated.

        Implementation Requirements:
        - Must update all render properties
        - Must maintain consistency with core state
        - Should be efficient (avoid unnecessary updates)
        """
        pass

    def validate(self) -> bool:
        """Validate element state consistency.

        Checks:
        1. Core state validity
        2. Render data validity
        3. Element-specific constraints

        Returns:
            bool: True if element state is valid
        """
        try:
            # Check core state
            if not isinstance(self._core, AtomCore):
                return False
            if not self._core.isValid():
                return False

            # Check render data
            if not isinstance(self._renderData, AtomData):
                return False

            # Element is valid
            return True
        except Exception:
            return False

    def _validate_args(self, args: dict[str, Any]) -> None:
        """Validate property update arguments.

        Args:
            args: Property updates to validate

        Raises:
            TypeError: If args has invalid types
            ValueError: If args has invalid values
        """
        if not isinstance(args, dict):
            raise TypeError(f'args must be dictionary, got {type(args)}')

        # Validate using Parsable helper
        required = self._get_required_args()
        if required:
            from ....utility import Parsable
            Parsable.validateRequiredArgs(
                args, required, f'{self.__class__.__name__}')

    def _get_required_args(self) -> list[str]:
        """Get required arguments for this element type.

        Returns:
            List of required property names

        Note:
            Override in subclasses to specify required properties
        """
        return []

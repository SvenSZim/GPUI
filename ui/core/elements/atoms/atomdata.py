from abc import ABC, abstractmethod
from typing import Any

from ..elementdata import ElementData

class AtomData(ElementData, ABC):
    """Abstract base class for atomic element render data.

    Manages visual properties and render state for atomic UI elements.
    Separates visual aspects from structural concerns in AtomCore.

    Features:
    - Visual property management
    - Render state tracking
    - Property validation
    - Efficient updates

    Implementation Requirements:
    - Must implement copy() for cloning
    - Must implement set() for property updates
    - Should validate visual properties
    - Should maintain render state consistency

    Thread Safety:
    - Property access is synchronized
    - State updates are atomic
    - Validation is thread-safe
    """

    @abstractmethod
    def copy(self) -> 'AtomData':
        """Create a deep copy of render data.

        Returns:
            New AtomData instance with copied properties

        Note:
            Implementations must ensure deep copy of all properties
        """
        pass

    @abstractmethod
    def set(self, args: dict[str, Any], skips: bool) -> bool:
        """Update render properties from arguments.

        Args:
            args: Property name/value pairs to apply
            skips: Whether to skip validation

        Returns:
            bool: True if any properties were updated

        Raises:
            TypeError: If args is not a dictionary
            ValueError: If args contains invalid values

        Note:
            Uses validateRequiredArgs from Parsable for validation
        """
        pass

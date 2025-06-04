from abc import ABC, abstractmethod
from typing import Any

from ..elementdata import ElementData

class AtomData(ElementData, ABC):
    """
    AtomData is the abstract base class for all render-related
    information of atom-elements.
    """
    @abstractmethod
    def copy(self) -> 'AtomData':
        pass

    # -------------------- access-point --------------------

    @abstractmethod
    def set(self, args: dict[str, Any]) -> bool:
        pass
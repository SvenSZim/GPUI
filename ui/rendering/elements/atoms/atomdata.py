from abc import ABC, abstractmethod

from ..elementdata import ElementData

class AtomData(ElementData, ABC):
    """
    AtomData is the abstract base class for all render-related
    information of atom-elements.
    """
    @abstractmethod
    def copy(self) -> 'AtomData':
        pass

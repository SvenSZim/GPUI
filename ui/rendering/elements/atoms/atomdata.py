from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from ..elementdata import ElementData
from .atomcreateoption import AtomCreateOption
from .atomprefab import AtomPrefab

CreateOption = TypeVar('CreateOption', bound=AtomCreateOption)
Prefab = TypeVar('Prefab', bound=AtomPrefab)

class AtomData(Generic[CreateOption, Prefab], ElementData[CreateOption, Prefab], ABC):
    """
    AtomData is the abstract base class for all render-related
    information of atom-elements.
    """
    @abstractmethod
    def copy(self) -> 'AtomData':
        pass

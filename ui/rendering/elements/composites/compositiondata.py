from abc import ABC
from typing import Generic, TypeVar

from ..elementdata import ElementData
from .compositioncreateoption import CompositionCreateOption
from .compositionprefab import CompositionPrefab

CreateOption = TypeVar('CreateOption', bound=CompositionCreateOption)
Prefab = TypeVar('Prefab', bound=CompositionPrefab)

class CompositionData(Generic[CreateOption, Prefab], ElementData[CreateOption, Prefab], ABC):
    """
    CompositionData is the abstract base class for all render-related
    information of composition-elements.
    """
 

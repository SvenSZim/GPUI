from abc import ABC
from typing import Generic, TypeVar

from ..compositiondata          import CompositionData
from .interactablecreateoption  import InteractableCreateOption
from .interactableprefab        import InteractablePrefab

CreateOption = TypeVar('CreateOption', bound=InteractableCreateOption)
Prefab = TypeVar('Prefab', bound=InteractablePrefab)

class InteractableData(Generic[CreateOption, Prefab], CompositionData[CreateOption, Prefab], ABC):
    pass

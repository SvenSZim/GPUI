from abc import ABC
from typing import Generic, TypeVar

from ...elementdata import ElementData
from .interactablecreateoption import InteractableCreateOption
from .interactableprefab import InteractablePrefab

CreateOption = TypeVar('CreateOption', bound=InteractableCreateOption)
Prefab = TypeVar('Prefab', bound=InteractablePrefab)

class InteractableData(Generic[CreateOption, Prefab], ElementData[CreateOption, Prefab], ABC):
    pass

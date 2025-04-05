from abc import ABC
from typing import Generic, TypeVar

from ..compositiondata  import CompositionData
from .addoncreateoption import AddonCreateOption
from .addonprefab       import AddonPrefab

CreateOption = TypeVar('CreateOption', bound=AddonCreateOption)
Prefab = TypeVar('Prefab', bound=AddonPrefab)

class AddonData(Generic[CreateOption, Prefab], CompositionData[CreateOption, Prefab], ABC):
    pass

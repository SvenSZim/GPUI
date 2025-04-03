from abc import ABC
from typing import Generic, TypeVar

from ...elementdata import ElementData
from .addoncreateoption import AddonCreateOption
from .addonprefab import AddonPrefab

CreateOption = TypeVar('CreateOption', bound=AddonCreateOption)
Prefab = TypeVar('Prefab', bound=AddonPrefab)

class AddonData(Generic[CreateOption, Prefab], ElementData[CreateOption, Prefab], ABC):
    pass

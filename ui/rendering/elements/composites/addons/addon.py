from abc import ABC
from typing import Generic, TypeVar, Union

from ...element         import Element
from .addoncore         import AddonCore
from .addondata         import AddonData
from .addoncreateoption import AddonCreateOption
from .addonprefab       import AddonPrefab

Inner = TypeVar('Inner', bound=Union[Element, list[Element]])

Core         = TypeVar('Core'        , bound=AddonCore        )
Data         = TypeVar('Data'        , bound=AddonData        )
CreateOption = TypeVar('CreateOption', bound=AddonCreateOption)
Prefab       = TypeVar('Prefab'      , bound=AddonPrefab      )

class Addon(Generic[Inner, Core, Data, CreateOption, Prefab], Element[Core, Data, CreateOption, Prefab], ABC):

    def __init__(self, core: Core, renderData: Data, active: bool = True) -> None:
        super().__init__(core, renderData, active)

from abc import ABC, abstractmethod
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

    def __init__(self, inner: Inner, renderData: Data, active: bool = True) -> None:
        core: Core = self._coreFromInner(inner)
        super().__init__(core, renderData, active)

    @staticmethod
    @abstractmethod
    def _coreFromInner(inner: Inner) -> Core:
        pass

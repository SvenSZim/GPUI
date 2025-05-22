from abc import ABC
from typing import Generic, TypeVar

from ...element     import Element
from .addoncore         import AddonCore
from .addondata         import AddonData

Core = TypeVar('Core', bound=AddonCore)
Data = TypeVar('Data', bound=AddonData)

class Addon(Generic[Core, Data], Element[Core, Data], ABC):

    def __init__(self, core: Core, renderData: Data, active: bool = True) -> None:
        super().__init__(core, renderData, active)

from abc import ABC
from typing import Generic, TypeVar, override

from ...element import Element
from .addoncore import AddonCore
from .addondata import AddonData

Core = TypeVar('Core', bound=AddonCore)
Data = TypeVar('Data', bound=AddonData)

class Addon(Generic[Core, Data], Element[Core, Data], ABC):

    def __init__(self, core: Core, renderData: Data, active: bool = True) -> None:
        super().__init__(core, renderData, active)

    @override
    def setActive(self, active: bool) -> None:
        super().setActive(active)
        self._core.setActive(active)

    @override
    def toggleActive(self) -> bool:
        bb = super().toggleActive()
        self._core.setActive(bb)
        return bb

    @override
    def setZIndex(self, zindex: int) -> None:
        super().setZIndex(zindex)
        self._core.setZIndex(zindex)
        self._renderData.setZIndex(zindex)

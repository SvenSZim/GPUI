from abc import ABC, abstractmethod
from typing import Any, Generic, override, TypeVar

from ..element         import Element
from .atomcore         import AtomCore
from .atomdata         import AtomData

Core         = TypeVar('Core'        , bound=AtomCore)
RenderData   = TypeVar('RenderData'  , bound=AtomData)

class Atom(Generic[Core, RenderData], Element[Core, RenderData], ABC):
    """
    Atom is the abstract base class for all ui-atom-elements.
    """

    # -------------------- creation --------------------

    def __init__(self, core: Core, renderData: RenderData, active: bool) -> None:
        super().__init__(core, renderData, active)

    @abstractmethod
    def copy(self) -> 'Atom':
        pass

    # -------------------- access-point --------------------

    @override
    def set(self, args: dict[str, Any], sets: int=-1, maxDepth: int=-1) -> int:
        """
        set is a general access point to an element. It has some basic functionality implemented and is overridden
        by some elements for more specific behavior (updating text in Text, subscribing to buttonpresses in button, etc.).
        set also recursivly applies the given args to all children until the given amount of
        'sets' or the maxDepth is reached. A 'set' is counted, if any of the given args can be applied to the element.

        Returns (int): the amount of 'sets' applied
        """
        s: bool = bool(super().set(args, sets, maxDepth))
        s |= self._core.set(args)
        s |= self._renderData.set(args)
        if s:
            self.updateRenderData()
        return int(s)

    # -------------------- rendering --------------------

    @override
    def forceUpdate(self) -> None:
        super().forceUpdate()
        self.updateRenderData()

    @abstractmethod
    def updateRenderData(self) -> None:
        pass
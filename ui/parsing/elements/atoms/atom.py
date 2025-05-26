from abc import ABC, abstractmethod
from typing import Generic, TypeVar

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

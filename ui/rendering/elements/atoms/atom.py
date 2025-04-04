from abc import ABC
from typing import Generic, TypeVar

from ..element         import Element
from .atomcore         import AtomCore
from .atomdata         import AtomData
from .atomcreateoption import AtomCreateOption
from .atomprefab       import AtomPrefab

AtomCls = TypeVar('AtomCls', bound='Atom')

Core         = TypeVar('Core'        , bound=AtomCore        )
RenderData   = TypeVar('RenderData'  , bound=AtomData        )
CreateOption = TypeVar('CreateOption', bound=AtomCreateOption)
Prefab       = TypeVar('Prefab'      , bound=AtomPrefab      )

class Atom(Generic[Core, RenderData, CreateOption, Prefab], Element[Core, RenderData, CreateOption, Prefab], ABC):
    """
    Atom is the abstract base class for all ui-atom-elements.
    """

    # -------------------- creation --------------------
    
    def __init__(self, core: Core, renderData: RenderData, active: bool) -> None:
        super().__init__(core, renderData, active)

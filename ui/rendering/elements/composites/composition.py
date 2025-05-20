from abc import ABC
from typing import Generic, TypeVar, override

from ..element      import Element
from .compositioncore           import CompositionCore
from .compositiondata           import CompositionData
from .compositioncreateoption   import CompositionCreateOption
from .compositionprefab         import CompositionPrefab

Core         = TypeVar('Core'        , bound=CompositionCore        )
RenderData   = TypeVar('RenderData'  , bound=CompositionData        )
CreateOption = TypeVar('CreateOption', bound=CompositionCreateOption)
Prefab       = TypeVar('Prefab'      , bound=CompositionPrefab      )

class Composition(Generic[Core, RenderData, CreateOption, Prefab], Element[Core, RenderData, CreateOption, Prefab], ABC):
    """
    Composition is the abstract base class for all ui-composition-elements.
    """

    # -------------------- creation --------------------
    
    def __init__(self, core: Core, renderData: RenderData, active: bool) -> None:
        super().__init__(core, renderData, active)

    @override
    def getInnerSizing(self, elSize: tuple[int, int]) -> tuple[int, int]:
        return self._core.getInnerSizing(elSize)

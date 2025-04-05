from abc import ABC
from typing import Generic, TypeVar

from ..composition      import Composition
from .interactablecore          import InteractableCore
from .interactabledata          import InteractableData
from .interactablecreateoption  import InteractableCreateOption
from .interactableprefab        import InteractablePrefab

Core         = TypeVar('Core'        , bound=InteractableCore        )
Data         = TypeVar('Data'        , bound=InteractableData        )
CreateOption = TypeVar('CreateOption', bound=InteractableCreateOption)
Prefab       = TypeVar('Prefab'      , bound=InteractablePrefab      )

class Interactable(Generic[Core, Data, CreateOption, Prefab], Composition[Core, Data, CreateOption, Prefab], ABC):

    def __init__(self, core: Core, renderData: Data, active: bool = True) -> None:
        super().__init__(core, renderData, active)

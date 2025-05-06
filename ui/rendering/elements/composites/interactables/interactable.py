from abc import ABC
from typing import Generic, TypeVar

from .....interaction import InputManager, InputEvent, Clickable
from ..composition      import Composition
from .interactablecore          import InteractableCore
from .interactabledata          import InteractableData
from .interactablecreateoption  import InteractableCreateOption
from .interactableprefab        import InteractablePrefab

Core         = TypeVar('Core'        , bound=InteractableCore        )
Data         = TypeVar('Data'        , bound=InteractableData        )
CreateOption = TypeVar('CreateOption', bound=InteractableCreateOption)
Prefab       = TypeVar('Prefab'      , bound=InteractablePrefab      )

class Interactable(Generic[Core, Data, CreateOption, Prefab], Composition[Core, Data, CreateOption, Prefab], Clickable, ABC):

    def __init__(self, core: Core, renderData: Data, renderActive: bool = True, buttonActive: bool=True) -> None:
        Composition.__init__(self, core, renderData, renderActive)
        Clickable.__init__(self, buttonActive)
        self._core.addTriggerEvent(self._onclick)
        
        #Default trigger event: LEFTDOWN
        self.addTriggerEvent(InputManager.getEvent(InputEvent.LEFTDOWN))

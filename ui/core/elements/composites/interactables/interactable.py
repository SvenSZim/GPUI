from abc import ABC
from typing import Any, Callable, TypeVar, override

from ...element         import Element
from .interactablecore  import InteractableCore
from .interactabledata  import InteractableData

Core = TypeVar('Core', bound=InteractableCore)
Data = TypeVar('Data', bound=InteractableData)

class Interactable(Element[Core, Data], ABC):
    """Abstract base class for interactive UI elements supporting click events and state changes.
    
    Provides common functionality for user-interactive elements including:
    - Click event handling and subscription
    - Active state management
    - Global and local trigger event system
    - Custom callback registration
    
    This class serves as the foundation for interactive elements like buttons,
    toggles, sliders, and other clickable/interactive UI components. It manages
    the interaction state and event handling while delegating rendering specifics
    to concrete implementations.
    """

    def __init__(self, core: Core, renderData: Data, renderActive: bool = True) -> None:
        Element.__init__(self, core, renderData, renderActive)

    # -------------------- active-state --------------------

    @override
    def setActive(self, active: bool) -> None:
        super().setActive(active)
        self._core.setButtonActive(active)

    @override
    def toggleActive(self) -> bool:
        bb = super().toggleActive()
        self._core.setButtonActive(bb)
        return bb

    # -------------------- access-point --------------------

    @override
    def _set(self, args: dict[str, Any], sets: int = -1, maxDepth: int = -1, skips: bool = False) -> bool:
        s: bool = super()._set(args, sets, maxDepth, skips)
        for tag, value in args.items():
            match tag:
                case 'setButtonActive':
                    s = True
                    if isinstance(value, bool):
                        self._core.setButtonActive(value)
                    else:
                        raise ValueError('setButtonActive expects a bool')
                case 'addTriggerEvent':
                    s = True
                    if not skips:
                        if isinstance(value, str):
                            self._core.addTriggerEvent(value)
                        else:
                            raise ValueError('addTriggerEvent expects a eventID')
                case 'removeTriggerEvent':
                    s = True
                    if not skips:
                        if isinstance(value, str):
                            self._core.removeTriggerEvent(value)
                        else:
                            raise ValueError('removeTriggerEvent expects a eventID')
                case 'addGlobalTriggerEvent':
                    s = True
                    if not skips:
                        if isinstance(value, str):
                            self._core.addGlobalTriggerEvent(value)
                        else:
                            raise ValueError('addGlobalTriggerEvent expects a eventID')
                case 'removeGlobalTriggerEvent':
                    s = True
                    if not skips:
                        if isinstance(value, str):
                            self._core.removeGlobalTriggerEvent(value)
                        else:
                            raise ValueError('removeGlobalTriggerEvent expects a eventID')
                case 'subscribeToClick':
                    s = True
                    if not skips:
                        if isinstance(value, str):
                            self._core.subscribeToClick(value)
                        else:
                            raise ValueError('subscribeToClick expects a callbackID')
                case 'unsubscribeToClick':
                    s = True
                    if not skips:
                        if isinstance(value, str):
                            self._core.unsubscribeToClick(value)
                        else:
                            raise ValueError('unsubscribeToClick expects a callbackID')
                case 'quickSubscribeToClick':
                    s = True
                    if not skips:
                        if isinstance(value, tuple) and isinstance(value[0], Callable) and isinstance(value[1], list):
                            self._core.quickSubscribeToClick(value[0], *value[1])
                        else:
                            raise ValueError('quickSubscribeToClick expects a 2-tuple with a Callable and a list of arguments')
        return s

from typing import Any, Callable, override

from ......utility  import Rect
from ......display  import Surface
from ......interaction  import InputEvent, InputManager
from ....element    import Element
from ..interactable import Interactable

from .elementcyclecore  import ElementCycleCore
from .elementcycledata  import ElementCycleData

class ElementCycle(Interactable[ElementCycleCore, ElementCycleData]):

    # -------------------- creation --------------------

    def __init__(self, rect: Rect, renderData: ElementCycleData, *inner: Element, startState: int=0, elementCycleActive: bool=True, active: bool = True) -> None:

        super().__init__(ElementCycleCore(rect, *inner, startState=startState, buttonActive=elementCycleActive), renderData, active)
    
    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'ElementCycle':
        button: ElementCycle = ElementCycle(Rect(), ElementCycleData.parseFromArgs(args), *args['inner'])
        hasTrigger: bool = False
        for tag, value in args.items():
            match tag:
                case 'trigger':
                    hasTrigger = True
                    for v in ElementCycle.parseList(value):
                        if v.lower() == 'click':
                            button._core.addTriggerEvent(InputManager.getEvent(InputEvent.LEFTDOWN))
                        else:
                            button._core.addTriggerEvent(InputManager.getEvent(InputEvent.fromStr(value)))
                case 'globaltrigger' | 'gtrigger' | 'global':
                    hasTrigger = True
                    for v in ElementCycle.parseList(value):
                        if v.lower() == 'click':
                            button._core.addGlobalTriggerEvent(InputManager.getEvent(InputEvent.LEFTDOWN))
                        else:
                            button._core.addGlobalTriggerEvent(InputManager.getEvent(InputEvent.fromStr(value)))
        if not hasTrigger:
            button._core.addTriggerEvent(InputManager.getEvent(InputEvent.LEFTDOWN))
        return button

    # -------------------- access-point --------------------

    @override
    def set(self, args: dict[str, Any]) -> None:
        super().set(args)
        for tag, value in args.items():
            match tag:
                case 'subscribeToToggleState':
                    if isinstance(value, tuple) and isinstance(value[0], int) and isinstance(value[1], str):
                        self._core.subscribeToToggleState(value[0], value[1])
                    else:
                        raise ValueError('subscribeToSelect expects 2-tuple with the toggle state (int) and a callbackID')
                case 'unsubscribeToToggleState':
                    if isinstance(value, tuple) and isinstance(value[0], int) and isinstance(value[1], str):
                        self._core.unsubscribeToToggleState(value[0], value[1])
                    else:
                        raise ValueError('unsubscribeToToggleState expects 2-tuple with the toggle state (int) and a callbackID')
                case 'quickSubscribeToToggleState':
                    if isinstance(value, tuple) and isinstance(value[0], int) and isinstance(value[1], Callable) and isinstance(value[2], list):
                        self._core.quickSubscribeToToggleState(value[0], value[1], *value[2])
                    else:
                        raise ValueError('quickSubscribeToToggleState expects a 3-tuple the toggle state (int), with a Callable and a list of arguments')
    
    # -------------------- rendering --------------------

    @override
    def render(self, surface: Surface) -> None:
        """
        render renders the UI-Element onto the given surface

        Args:
            surface (Surface): the surface the UIElement should be drawn on
        """
        assert self._drawer is not None

        if not self._active:
            return
    
        self._core.getCurrentElement().render(surface)

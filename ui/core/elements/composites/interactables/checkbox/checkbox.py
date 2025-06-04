from typing import Any, Callable, override

from ......utility      import Rect
from ......display      import Surface
from ......interaction  import InputEvent, InputManager
from ..interactable     import Interactable

from .checkboxcore      import CheckboxCore
from .checkboxdata      import CheckboxData

class Checkbox(Interactable[CheckboxCore, CheckboxData]):

    # -------------------- creation --------------------

    def __init__(self, rect: Rect, renderData: CheckboxData, startState: bool=False, checkboxActive: bool=True, active: bool = True) -> None:

        super().__init__(CheckboxCore(rect, startState, checkboxActive), renderData, active)
        self._renderData.alignInner(self)
    
    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'Checkbox':
        button: Checkbox = Checkbox(Rect(), CheckboxData.parseFromArgs(args))
        hasTrigger: bool = False
        for tag, value in args.items():
            match tag:
                case 'trigger':
                    hasTrigger = True
                    for v in Checkbox.parseList(value):
                        if v.lower() == 'click':
                            button._core.addTriggerEvent(InputManager.getEvent(InputEvent.LEFTDOWN))
                        else:
                            button._core.addTriggerEvent(InputManager.getEvent(InputEvent.fromStr(value)))
                case 'globaltrigger' | 'gtrigger' | 'global':
                    hasTrigger = True
                    for v in Checkbox.parseList(value):
                        if v.lower() == 'click':
                            button._core.addGlobalTriggerEvent(InputManager.getEvent(InputEvent.LEFTDOWN))
                        else:
                            button._core.addGlobalTriggerEvent(InputManager.getEvent(InputEvent.fromStr(value)))
        if not hasTrigger:
            button._core.addTriggerEvent(InputManager.getEvent(InputEvent.LEFTDOWN))
        return button

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
        super().set(args)
        for tag, value in args.items():
            match tag:
                case 'subscribeToSelect':
                    if isinstance(value, str):
                        self._core.subscribeToToggleState(1, value)
                    else:
                        raise ValueError('subscribeToSelect expects a callbackID')
                case 'unsubscribeToSelect':
                    if isinstance(value, str):
                        self._core.unsubscribeToToggleState(1, value)
                    else:
                        raise ValueError('unsubscribeToSelect expects a callbackID')
                case 'quickSubscribeToSelect':
                    if isinstance(value, tuple) and isinstance(value[0], Callable) and isinstance(value[1], list):
                        self._core.quickSubscribeToToggleState(1, value[0], *value[1])
                    else:
                        raise ValueError('quickSubscribeToSelect expects a 2-tuple with a Callable and a list of arguments')
                case 'subscribeToDeselect':
                    if isinstance(value, str):
                        self._core.subscribeToToggleState(0, value)
                    else:
                        raise ValueError('subscribeToDeselect expects a callbackID')
                case 'unsubscribeToDeselect':
                    if isinstance(value, str):
                        self._core.unsubscribeToToggleState(0, value)
                    else:
                        raise ValueError('unsubscribeToDeselect expects a callbackID')
                case 'quickSubscribeToDeselect':
                    if isinstance(value, tuple) and isinstance(value[0], Callable) and isinstance(value[1], list):
                        self._core.quickSubscribeToToggleState(0, value[0], *value[1])
                    else:
                        raise ValueError('quickSubscribeToDeselect expects a 2-tuple with a Callable and a list of arguments')

    # -------------------- rendering --------------------

    @override
    def render(self, surface: Surface) -> None:
        """
        render renders the UI-Element onto the given surface

        Args:
            surface (Surface): the surface the UIElement should be drawn on
        """
        assert self._drawer is not None

        if self._core.getCurrentToggleState():
            self._renderData.fillData.render(surface)
            self._renderData.crossData[0].render(surface)
            self._renderData.crossData[1].render(surface)

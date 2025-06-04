from typing import Any, Callable, override

from ......display   import Surface
from ......interaction  import InputEvent, InputManager
from ....element     import Element
from ..interactable  import Interactable

from .togglewrappercore         import TogglewrapperCore
from .togglewrapperdata         import TogglewrapperData

class Togglewrapper(Interactable[TogglewrapperCore, TogglewrapperData]):

    # -------------------- creation --------------------

    def __init__(self, inner: Element, numberOfStates: int=2, startState: int=0, buttonActive: bool=True, active: bool = True) -> None:
        
        super().__init__(TogglewrapperCore(inner, numberOfStates, startState, buttonActive), TogglewrapperData(), renderActive=active)
    
    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'Togglewrapper':
        button: Togglewrapper = Togglewrapper(args['inner'])
        hasTrigger: bool = False
        for tag, value in args.items():
            match tag:
                case 'trigger':
                    hasTrigger = True
                    for v in Togglewrapper.parseList(value):
                        if v.lower() == 'click':
                            button._core.addTriggerEvent(InputManager.getEvent(InputEvent.LEFTDOWN))
                        else:
                            button._core.addTriggerEvent(InputManager.getEvent(InputEvent.fromStr(value)))
                case 'globaltrigger' | 'gtrigger' | 'global':
                    hasTrigger = True
                    for v in Togglewrapper.parseList(value):
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
        return 0

    # -------------------- rendering --------------------

    @override
    def render(self, surface: Surface) -> None:
        """
        render renders the UI-Element onto the given surface

        Args:
            surface (Surface): the surface the UIElement should be drawn on
        """
        assert self._drawer is not None

        if self.isActive():
            if self._core.getCurrentToggleState():
                self._drawer.drawrect(surface, self.getRect(), 'green')
            self._core.getInner().render(surface)

from typing import Any, Callable, override

from ......utility   import Rect
from ......display   import Surface
from ......interaction import InputEvent, InputManager
from ..interactable  import Interactable

from .buttoncore         import ButtonCore
from .buttondata         import ButtonData

class Button(Interactable[ButtonCore, ButtonData]):

    # -------------------- creation --------------------

    def __init__(self, rect: Rect, renderData: ButtonData, buttonActive: bool=True, active: bool = True) -> None:

        super().__init__(ButtonCore(rect, buttonActive), renderData, active)
        
        self._renderData.alignInner(self)
    
    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'Button':
        button: Button = Button(Rect(), ButtonData.parseFromArgs(args))
        hasTrigger: bool = False
        for tag, value in args.items():
            match tag:
                case 'trigger':
                    hasTrigger = True
                    for v in Button.parseList(value):
                        if v.lower() == 'click':
                            button._core.addTriggerEvent(InputManager.getEvent(InputEvent.LEFTDOWN))
                            button._core.addReleaseEvent(InputManager.getEvent(InputEvent.LEFTUP))
                        else:
                            button._core.addTriggerEvent(InputManager.getEvent(InputEvent.fromStr(value)))
                            button._core.addReleaseEvent(InputManager.getEvent(InputEvent(InputEvent.fromStr(value).value+1)))
                case 'globaltrigger' | 'gtrigger' | 'global':
                    hasTrigger = True
                    for v in Button.parseList(value):
                        if v.lower() == 'click':
                            button._core.addGlobalTriggerEvent(InputManager.getEvent(InputEvent.LEFTDOWN))
                            button._core.addReleaseEvent(InputManager.getEvent(InputEvent.LEFTUP))
                        else:
                            button._core.addGlobalTriggerEvent(InputManager.getEvent(InputEvent.fromStr(value)))
                            button._core.addReleaseEvent(InputManager.getEvent(InputEvent(InputEvent.fromStr(value).value+1)))
        if not hasTrigger:
            button._core.addTriggerEvent(InputManager.getEvent(InputEvent.LEFTDOWN))
            button._core.addReleaseEvent(InputManager.getEvent(InputEvent.LEFTUP))
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
                case 'subscribeToHold':
                    if isinstance(value, str):
                        self._core.subscribeToHold(value)
                    else:
                        raise ValueError('subscribeToHold expects a callbackID')
                case 'unsubscribeToHold':
                    if isinstance(value, str):
                        self._core.unsubscribeToHold(value)
                    else:
                        raise ValueError('unsubscribeToHold expects a callbackID')
                case 'quickSubscribeToHold':
                    if isinstance(value, tuple) and isinstance(value[0], Callable) and isinstance(value[1], list):
                        self._core.quickSubscribeToHold(value[0], *value[1])
                    else:
                        raise ValueError('quickSubscribeToHold expects a 2-tuple with a Callable and a list of arguments')

    # -------------------- rendering --------------------

    @override
    def render(self, surface: Surface) -> None:
        """
        render renders the UI-Element onto the given surface

        Args:
            surface (Surface): the surface the UIElement should be drawn on
        """
        assert self._drawer is not None

        if self._active:
            if self._core.isPressed():
                self._renderData.fillData.render(surface)
                self._renderData.crossData[0].render(surface)
                self._renderData.crossData[1].render(surface)

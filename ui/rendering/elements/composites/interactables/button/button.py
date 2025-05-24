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
    def set(self, args: dict[str, Any]) -> None:
        super().set(args)
        for tag, value in args.items():
            match tag:
                case 'subscribeToClick':
                    if isinstance(value, str):
                        self._core.subscribeToClick(value)
                    else:
                        raise ValueError('subscribeToClick expects a callbackID')
                case 'unsubscribeToClick':
                    if isinstance(value, str):
                        self._core.unsubscribeToClick(value)
                    else:
                        raise ValueError('unsubscribeToClick expects a callbackID')
                case 'quickSubscribeToClick':
                    if isinstance(value, tuple) and isinstance(value[0], Callable) and isinstance(value[1], list):
                        self._core.quickSubscribeToClick(value[0], *value[1])
                    else:
                        raise ValueError('quickSubscribeToClick expects a 2-tuple with a Callable and a list of arguments')
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

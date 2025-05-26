from typing import Any, Callable, override

from ......display   import Surface
from ......interaction  import InputEvent, InputManager
from ....element     import Element
from ..interactable  import Interactable

from .clickwrappercore         import ClickwrapperCore
from .clickwrapperdata         import ClickwrapperData

class Clickwrapper(Interactable[ClickwrapperCore, ClickwrapperData]):

    # -------------------- creation --------------------

    def __init__(self, inner: Element, buttonActive: bool=True, active: bool = True) -> None:

        super().__init__(ClickwrapperCore(inner, buttonActive), ClickwrapperData(), renderActive=active)
    
    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'Clickwrapper':
        button: Clickwrapper = Clickwrapper(args['inner'])
        hasTrigger: bool = False
        for tag, value in args.items():
            match tag:
                case 'trigger':
                    hasTrigger = True
                    for v in Clickwrapper.parseList(value):
                        if v.lower() == 'click':
                            button._core.addTriggerEvent(InputManager.getEvent(InputEvent.LEFTDOWN))
                            button._core.addReleaseEvent(InputManager.getEvent(InputEvent.LEFTUP))
                        else:
                            button._core.addTriggerEvent(InputManager.getEvent(InputEvent.fromStr(value)))
                            button._core.addReleaseEvent(InputManager.getEvent(InputEvent(InputEvent.fromStr(value).value+1)))
                case 'globaltrigger' | 'gtrigger' | 'global':
                    hasTrigger = True
                    for v in Clickwrapper.parseList(value):
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

        if self.isActive():
            if self._core.getButtonActive():
                self._core.getInner().render(surface)
            else:
                self._drawer.drawrect(surface, self.getRect(), "red")

from typing import Any, Callable, Optional, override

from ......utility      import StyledDefault
from ......display      import Surface
from ......interaction  import InputEvent, InputManager

from ....element    import Element
from ....atoms      import Box
from ..interactable import Interactable

from .buttoncore    import ButtonCore
from .buttondata    import ButtonData

class Button(Interactable[ButtonCore, ButtonData]):
    """A basic interactive button element with press and hold states.
    
    The Button provides a clickable interface element that:
    - Supports different visual states for normal and pressed states
    - Handles click and hold interactions
    - Supports both local and global trigger events
    - Manages custom callback subscriptions
    - Can be styled through the style system
    
    Buttons serve as the primary interaction point in UIs, used for:
    - Action triggers (e.g., submit, cancel)
    - Navigation controls
    - State toggles with visual feedback
    - Hold-to-activate functionality
    """

    # -------------------- creation --------------------

    def __init__(self, off: Element, on: Optional[Element], buttonActive: bool=True, active: bool = True) -> None:
        super().__init__(ButtonCore(buttonActive), ButtonData(off, on), active)
        
        self._renderData.alignInner(self)
    
    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'Button':
        inner: list[Element] = args['inner']
        style: str = args['fixstyle']
        off: Element
        on: Optional[Element]
        bactive: bool = True
        match len(inner):
            case 0:
                poff: Optional[Element] = Button.getStyledElement(args['off'], style) if 'off' in args else\
                                          Button.getStyledElement(StyledDefault.BUTTON_OFF, style)
                off = Box.parseFromArgs({}) if poff is None else poff
                on = Button.getStyledElement(args['off'], style) if 'off' in args else\
                     Button.getStyledElement(StyledDefault.BUTTON_ON, style)
            case 1:
                off = inner[0]
                on = Button.getStyledElement(args['off'], style) if 'off' in args else\
                     Button.getStyledElement(StyledDefault.BUTTON_ON, style)
            case _:
                off = inner[0]
                on = inner[1]

        button: Button = Button(off, on, buttonActive=bactive)
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
    def _set(self, args: dict[str, Any], sets: int = -1, maxDepth: int = -1, skips: bool = False) -> bool:
        s: bool = super()._set(args, sets, maxDepth, skips)
        for tag, value in args.items():
            match tag:
                case 'subscribeToHold':
                    s = True
                    if not skips:
                        if isinstance(value, str):
                            self._core.subscribeToHold(value)
                        else:
                            raise ValueError('subscribeToHold expects a callbackID')
                case 'unsubscribeToHold':
                    s = True
                    if not skips:
                        if isinstance(value, str):
                            self._core.unsubscribeToHold(value)
                        else:
                            raise ValueError('unsubscribeToHold expects a callbackID')
                case 'quickSubscribeToHold':
                    s = True
                    if not skips:
                        if isinstance(value, tuple) and isinstance(value[0], Callable) and isinstance(value[1], list):
                            self._core.quickSubscribeToHold(value[0], *value[1])
                        else:
                            raise ValueError('quickSubscribeToHold expects a 2-tuple with a Callable and a list of arguments')
                case 'buttonCheck':
                    s = True
                    if not skips:
                        if isinstance(value, tuple) and isinstance(value[0], Callable) and isinstance(value[1], list):
                            value[0](*value[1])
                        else:
                            raise ValueError('buttonCheck expects a 2-tuple with a Callable and a list of arguments')
        return s
    
    @override
    def set(self, args: dict[str, Any], sets: int = -1, maxDepth: int = -1, skips: list[int] = [0]) -> int:
        """
        set is a general access point to an element. It has some basic functionality implemented and is overridden
        by some elements for more specific behavior (updating text in Text, subscribing to buttonpresses in button, etc.).
        set also recursivly applies the given args to all children until the given amount of
        'sets' or the maxDepth is reached. A 'set' is counted, if any of the given args can be applied to the element.

        Returns (int): the amount of 'sets' applied
        """
        ts: int = 0
        s: bool = self._set(args, sets, maxDepth, bool(skips[0]))
        ts += int(s and not skips[0])
        if 0 <= maxDepth < 2:
            return ts
        skips[0] = max(0, skips[0]-ts)
        if sets < 0 or ts < sets:
            cs: int = self._renderData.setinner(args, sets-ts, maxDepth-1, skips)
            skips[0] = max(0, skips[0]-cs)
            ts += cs
        return ts

    # -------------------- rendering --------------------

    @override
    def setZIndex(self, zindex: int) -> None:
        super().setZIndex(zindex)
        self._renderData.off.setZIndex(zindex)
        if self._renderData.on:
            self._renderData.on.setZIndex(zindex)
        self._core.setPriority(zindex)

    @override
    def render(self, surface: Surface) -> None:
        """
        render renders the UI-Element onto the given surface

        Args:
            surface (Surface): the surface the UIElement should be drawn on
        """
        assert self._drawer is not None

        if self._active:
            if self._renderData.on is not None and self._core.isPressed():
                self._renderData.on.render(surface)
            else:
                self._renderData.off.render(surface)

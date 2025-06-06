from typing import Any, Callable, Optional, override

from ......utility  import StyledDefault
from ......display  import Surface
from ......interaction  import InputEvent, InputManager
from ....element    import Element
from ....atoms      import Box
from ..interactable import Interactable

from .togglecore  import ToggleCore
from .toggledata  import ToggleData

class Toggle(Interactable[ToggleCore, ToggleData]):

    # -------------------- creation --------------------

    def __init__(self, renderData: ToggleData, startState: int=0, toggleActive: bool=True, active: bool = True) -> None:
        super().__init__(ToggleCore(len(renderData.stateElements), startState=startState, buttonActive=toggleActive), renderData, active)
        renderData.alignInner(self)
        self._core.quickSubscribeToClick(self.changeState)
    
    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'Toggle':
        typ: str = args['typ']
        inner: list[Element] = args['inner']
        style: str = args['fixstyle']
        data: ToggleData
        match typ:
            case 'checkbox':
                off: Element
                on: Element
                match len(inner):
                    case 0:
                        poff: Optional[Element] = Toggle.getStyledElement(args['off'], style) if 'off' in args else\
                                                  Toggle.getStyledElement(StyledDefault.CHECKBOX_OFF, style)
                        off = Box.parseFromArgs({}) if poff is None else poff
                        pon: Optional[Element] = Toggle.getStyledElement(args['off'], style) if 'off' in args else\
                                                 Toggle.getStyledElement(StyledDefault.CHECKBOX_ON, style)
                        on = Box.parseFromArgs({}) if pon is None else pon
                    case 1:
                        off = inner[0]
                        pon: Optional[Element] = Toggle.getStyledElement(args['off'], style) if 'off' in args else\
                                                 Toggle.getStyledElement(StyledDefault.CHECKBOX_ON, style)
                        on = Box.parseFromArgs({}) if pon is None else pon
                    case _:
                        off = inner[0]
                        on = inner[1]
                data = ToggleData([off, on])
            case _:
                rawContent: str = args['content'].strip()
                if len(rawContent) > 0:
                    for opt in Toggle.parseList(rawContent):
                        newEl: Optional[Element] = Toggle.getStyledElement(args['textbox'], style) if 'textbox' in args else\
                                                   Toggle.getStyledElement(StyledDefault.TEXTBOX, style)
                        if newEl is not None:
                            newEl.set({'content':opt}, sets=1)
                            inner.append(newEl)
                data = ToggleData(inner)
        for el in data.stateElements[1:]:
            el.setActive(False)

        bactive: bool = True
        button: Toggle = Toggle(data, toggleActive=bactive)
        
        hasTrigger: bool = False
        for tag, value in args.items():
            match tag:
                case 'trigger':
                    hasTrigger = True
                    for v in Toggle.parseList(value):
                        if v.lower() == 'click':
                            button._core.addTriggerEvent(InputManager.getEvent(InputEvent.LEFTDOWN))
                        else:
                            button._core.addTriggerEvent(InputManager.getEvent(InputEvent.fromStr(value)))
                case 'globaltrigger' | 'gtrigger' | 'global':
                    hasTrigger = True
                    for v in Toggle.parseList(value):
                        if v.lower() == 'click':
                            button._core.addGlobalTriggerEvent(InputManager.getEvent(InputEvent.LEFTDOWN))
                        else:
                            button._core.addGlobalTriggerEvent(InputManager.getEvent(InputEvent.fromStr(value)))
        if not hasTrigger:
            button._core.addTriggerEvent(InputManager.getEvent(InputEvent.LEFTDOWN))
        return button

    # -------------------- state-change --------------------

    def changeState(self) -> None:
        for el in self._renderData.stateElements:
            el.setActive(False)
        self._renderData.stateElements[self._core.getCurrentToggleState()].setActive(True)

    # -------------------- access-point --------------------

    @override
    def _set(self, args: dict[str, Any], sets: int = -1, maxDepth: int = -1, skips: bool = False) -> bool:
        s: bool = super()._set(args, sets, maxDepth, skips)
        for tag, value in args.items():
            match tag:
                case 'subscribeToToggleState':
                    s = True
                    if not skips:
                        if isinstance(value, tuple) and isinstance(value[0], int) and isinstance(value[1], str):
                            self._core.subscribeToToggleState(value[0], value[1])
                        else:
                            raise ValueError('subscribeToSelect expects 2-tuple with the toggle state (int) and a callbackID')
                case 'unsubscribeToToggleState':
                    s = True
                    if not skips:
                        if isinstance(value, tuple) and isinstance(value[0], int) and isinstance(value[1], str):
                            self._core.unsubscribeToToggleState(value[0], value[1])
                        else:
                            raise ValueError('unsubscribeToToggleState expects 2-tuple with the toggle state (int) and a callbackID')
                case 'quickSubscribeToToggleState':
                    s = True
                    if not skips:
                        if isinstance(value, tuple) and isinstance(value[0], int) and isinstance(value[1], Callable) and isinstance(value[2], list):
                            self._core.quickSubscribeToToggleState(value[0], value[1], *value[2])
                        else:
                            raise ValueError('quickSubscribeToToggleState expects a 3-tuple the toggle state (int), with a Callable and a list of arguments')
                case 'toggleCheck':
                    s = True
                    if not skips:
                        if isinstance(value, tuple) and isinstance(value[0], Callable) and isinstance(value[1], list):
                            value[0](*value[1])
                        else:
                            raise ValueError('toggleCheck expects a 2-tuple with a Callable and a list of arguments')
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
    def render(self, surface: Surface) -> None:
        """
        render renders the UI-Element onto the given surface

        Args:
            surface (Surface): the surface the UIElement should be drawn on
        """
        assert self._drawer is not None

        if self._active:
            self._renderData.stateElements[self._core.getCurrentToggleState()].render(surface)

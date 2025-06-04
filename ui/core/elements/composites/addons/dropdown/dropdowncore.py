from typing import Any, Optional, override

from ......utility      import AlignType, Parsable, Rect
from ......interaction  import InputEvent, InputManager, Togglable
from ....element    import Element
from ..grouped      import Grouped
from ..addoncore    import AddonCore

class DropdownCore(AddonCore[Element], Togglable):
    """
    DropdownCore is the core object of the addon 'Dropdown'.
    """

    def __init__(self, inner: Element, buttonActive: bool=True) -> None:
        AddonCore.__init__(self, inner.getRect(), inner)
        Togglable.__init__(self, numberOfStates=2, buttonActive=buttonActive)

    @override
    def getInnerSizing(self, elSize: tuple[int, int], args: dict[str, Any]) -> tuple[int, int]:
        return self._inner.getInnerSizing(elSize)

    @override
    def _alignInner(self) -> None:
        self._inner.align(self)
        self._inner.alignSize(self)

    @override
    def setActive(self, active: bool) -> None:
        self.setButtonActive(active)
        self._inner.setActive(active)

    def adjustFromArgs(self, args: dict[str, Any], hasTrigger: bool=True) -> None:
        for tag, value in args.items():
            match tag:
                case 'trigger':
                    hasTrigger = True
                    for v in Parsable.parseList(value):
                        if v.lower() == 'click':
                            self.addTriggerEvent(InputManager.getEvent(InputEvent.LEFTDOWN))
                        else:
                            self.addTriggerEvent(InputManager.getEvent(InputEvent.fromStr(value)))
                case 'globaltrigger' | 'gtrigger' | 'global':
                    hasTrigger = True
                    for v in Parsable.parseList(value):
                        if v.lower() == 'click':
                            self.addGlobalTriggerEvent(InputManager.getEvent(InputEvent.LEFTDOWN))
                        else:
                            self.addGlobalTriggerEvent(InputManager.getEvent(InputEvent.fromStr(value)))
        if not hasTrigger:
            self.addTriggerEvent(InputManager.getEvent(InputEvent.LEFTDOWN))

    # -------------------- access-point --------------------

    def set(self, args: dict[str, Any]) -> bool:
        s: bool = False
        for tag, value in args.items():
            match tag:
                case 'setButtonActive':
                    s = True
                    if isinstance(value, bool):
                        self.setButtonActive(value)
                    else:
                        raise ValueError('setButtonActive expects a bool')
                case 'addTriggerEvent':
                    s = True
                    if isinstance(value, str):
                        self.addTriggerEvent(value)
                    else:
                        raise ValueError('addTriggerEvent expects a eventID')
                case 'removeTriggerEvent':
                    s = True
                    if isinstance(value, str):
                        self.removeTriggerEvent(value)
                    else:
                        raise ValueError('removeTriggerEvent expects a eventID')
                case 'addGlobalTriggerEvent':
                    s = True
                    if isinstance(value, str):
                        self.addGlobalTriggerEvent(value)
                    else:
                        raise ValueError('addGlobalTriggerEvent expects a eventID')
                case 'removeGlobalTriggerEvent':
                    s = True
                    if isinstance(value, str):
                        self.removeGlobalTriggerEvent(value)
                    else:
                        raise ValueError('removeGlobalTriggerEvent expects a eventID')
                case 'subscribeToClick':
                    s = True
                    if isinstance(value, str):
                        self.subscribeToClick(value)
                    else:
                        raise ValueError('subscribeToClick expects a callbackID')
                case 'unsubscribeToClick':
                    s = True
                    if isinstance(value, str):
                        self.unsubscribeToClick(value)
                    else:
                        raise ValueError('unsubscribeToClick expects a callbackID')
                case 'quickSubscribeToClick':
                    s = True
                    if isinstance(value, tuple) and isinstance(value[0], Callable) and isinstance(value[1], list):
                        self.quickSubscribeToClick(value[0], *value[1])
                    else:
                        raise ValueError('quickSubscribeToClick expects a 2-tuple with a Callable and a list of arguments')
                case 'subscribeToSelect':
                    s = True
                    if isinstance(value, str):
                        self.subscribeToToggleState(1, value)
                    else:
                        raise ValueError('subscribeToSelect expects a callbackID')
                case 'unsubscribeToSelect':
                    s = True
                    if isinstance(value, str):
                        self.unsubscribeToToggleState(1, value)
                    else:
                        raise ValueError('unsubscribeToSelect expects a callbackID')
                case 'quickSubscribeToSelect':
                    s = True
                    if isinstance(value, tuple) and isinstance(value[0], Callable) and isinstance(value[1], list):
                        self.quickSubscribeToToggleState(1, value[0], *value[1])
                    else:
                        raise ValueError('quickSubscribeToSelect expects a 2-tuple with a Callable and a list of arguments')
                case 'subscribeToDeselect':
                    s = True
                    if isinstance(value, str):
                        self.subscribeToToggleState(0, value)
                    else:
                        raise ValueError('subscribeToDeselect expects a callbackID')
                case 'unsubscribeToDeselect':
                    s = True
                    if isinstance(value, str):
                        self.unsubscribeToToggleState(0, value)
                    else:
                        raise ValueError('unsubscribeToDeselect expects a callbackID')
                case 'quickSubscribeToDeselect':
                    s = True
                    if isinstance(value, tuple) and isinstance(value[0], Callable) and isinstance(value[1], list):
                        self.quickSubscribeToToggleState(0, value[0], *value[1])
                    else:
                        raise ValueError('quickSubscribeToDeselect expects a 2-tuple with a Callable and a list of arguments')
        return s

    def setinner(self, args: dict[str, Any], sets: int=-1, maxDepth: int=-1) -> int:
        return self._inner.set(args, sets, maxDepth)
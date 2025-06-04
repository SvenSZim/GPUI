from typing import Any, override

from ......utility      import Rect, Parsable
from ......interaction  import Togglable, InputEvent, InputManager
from ....element        import Element
from ....atoms          import Box, Text, Line
from ...addons          import Framed, Dropdown
from ..interactablecore import InteractableCore
from ..clickwrapper     import Clickwrapper

class DropdownselectCore(InteractableCore, Togglable):
    """
    DropdownselectCore is the core object of the interactable 'Dropdownselect'.
    """
    # -------------------- setup --------------------
    __outer: list[Element]
    __dropdown: Dropdown

    def __init__(self, rect: Rect, heads: list[Element], opts: list[Element], startState: int=0, buttonActive: bool=True, **dpdkwargs) -> None:
        InteractableCore.__init__(self, rect)
        Togglable.__init__(self, numberOfStates=len(opts)+1, startState=startState, buttonActive=buttonActive)

        self.__outer = heads
        self.__innerSetup(opts, **dpdkwargs)

    def __innerSetup(self, inner: list[Element], **kwargs) -> None:
        innerSelectors: list[Clickwrapper] = []
        self.__outer.insert(0, Framed.parseFromArgs({'inner':[Text.parseFromArgs({'col':'white', 'content':'SELECT', 'siz':'m'}), Line.parseFromArgs({'col':'white'})]}))
        for nr, el in enumerate(inner):
            newSelector: Clickwrapper = Clickwrapper(el, buttonActive=False)
            newSelector.set({'quickSubscribeToClick':(self._onCustomTrigger, [lambda _, k=nr+1: k])})
            innerSelectors.append(newSelector)

        for el in self.__outer:
            el.align(self)
            el.alignSize(self)

        hasTrigger: bool = False
        for tag, value in kwargs.items():
            match tag:
                case 'trigger':
                    hasTrigger = True
                    for v in Parsable.parseList(value):
                        event: str = ''
                        if v.lower() == 'click':
                            event = InputManager.getEvent(InputEvent.LEFTDOWN)
                        else:
                            event = InputManager.getEvent(InputEvent.fromStr(v))
                        for s in innerSelectors:
                            s.set({'addTriggerEvent':event})
        if not hasTrigger:
            event = InputManager.getEvent(InputEvent.LEFTDOWN)
            for s in innerSelectors:
                s.set({'addTriggerEvent':event})

        innerSelectors.insert(0, Box.parseFromArgs({}))
        kwargs['inner'] = innerSelectors
        self.__dropdown = Dropdown.parseFromArgs(kwargs)

        self.__dropdown.set({'removeTriggerEvent':InputManager.getEvent(InputEvent.LEFTDOWN)})
        self.__dropdown.set({'addGlobalTriggerEvent':self._onclick})

        self.__dropdown.align(self)
        self.__dropdown.alignSize(self)

    # -------------------- getter --------------------

    def getOuter(self) -> Element:
        return self.__outer[self.getCurrentToggleState()]

    def getDropdown(self) -> Dropdown:
        return self.__dropdown

    @override
    def getInnerSizing(self, elSize: tuple[int, int], args: dict[str, Any]) -> tuple[int, int]:
        maxWidth, maxHeight = 0, 0
        for el in self.__outer:
            x, y = el.getInnerSizing(elSize)
            if x > maxWidth:
                maxWidth = x
            if y > maxHeight:
                maxHeight = y
        return maxWidth, maxHeight

    # -------------------- setter --------------------

    @override
    def addTriggerEvent(self, event: str) -> bool:
        self.__dropdown.set({'addTriggerEvent':event})
        return True

    @override
    def removeTriggerEvent(self, event: str) -> bool:
        self.__dropdown.set({'removeTriggerEvent':event})
        return True

    @override
    def addGlobalTriggerEvent(self, event: str) -> bool:
        self.__dropdown.set({'addGlobalTriggerEvent':event})
        return True

    @override
    def removeGlobalTriggerEvent(self, event: str) -> bool:
        self.__dropdown.set({'removeGlobalTriggerEvent':event})
        return True

    # -------------------- active-state --------------------

    @override
    def setButtonActive(self, buttonActive: bool) -> None:
        super().setButtonActive(buttonActive)
        self.__dropdown.setActive(buttonActive)


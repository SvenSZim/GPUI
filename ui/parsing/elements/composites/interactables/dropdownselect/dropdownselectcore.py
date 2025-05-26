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
    __innerSelectors: list[Clickwrapper]
    __outer: list[Element]
    __dropdown: Dropdown

    def __init__(self, rect: Rect, *inner: tuple[tuple[Element, float], Element], verticalDropdown: bool=True, offset: int=0,
                 startState: int=0, buttonActive: bool=True, args: dict[str, Any]={}) -> None:
        InteractableCore.__init__(self, rect)
        Togglable.__init__(self, numberOfStates=len(inner)+1, startState=startState, buttonActive=buttonActive)


        self.__dropdown = Dropdown(Box.parseFromArgs({}), *self.__innerSetup(*inner, **args), verticalDropdown=verticalDropdown, offset=offset, dropdownActive=buttonActive)
        self.__dropdown.set({'removeTriggerEvent':InputManager.getEvent(InputEvent.LEFTDOWN)})
        self.__dropdown.set({'addGlobalTriggerEvent':self._onclick})

        self.__dropdown.align(self)
        self.__dropdown.alignSize(self)

    def __innerSetup(self, *inner: tuple[tuple[Element, float], Element], **kwargs) -> list[tuple[Clickwrapper, float]]:
        self.__innerSelectors = []
        sizedSelectors: list[tuple[Clickwrapper, float]] = []
        self.__outer = [Framed.parseFromArgs({'inner':[Text.parseFromArgs({'col':'white', 'content':'SELECT', 'siz':'m'}), Line.parseFromArgs({'col':'white'})]})]
        for nr, (el, head) in enumerate(inner):
            newSelector: Clickwrapper = Clickwrapper(el[0], buttonActive=False)
            newSelector.set({'quickSubscribeToClick':(self._onCustomTrigger, [lambda _, k=nr+1: k])})
            sizedSelectors.append((newSelector, el[1]))
            self.__innerSelectors.append(newSelector)
            self.__outer.append(head)
 
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
                        for s in self.__innerSelectors:
                            s.set({'addTriggerEvent':event})
        if not hasTrigger:
            event = InputManager.getEvent(InputEvent.LEFTDOWN)
            for s in self.__innerSelectors:
                s.set({'addTriggerEvent':event})
        return sizedSelectors

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


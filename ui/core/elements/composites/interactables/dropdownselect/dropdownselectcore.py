from typing import Any, override

from ......utility      import Rect, Parsable
from ......interaction  import Togglable, InputEvent, InputManager
from ....element        import Element
from ....atoms          import Box
from ...addons          import Dropdown
from ..interactablecore import InteractableCore

class DropdownselectCore(InteractableCore, Togglable):
    """
    DropdownselectCore is the core object of the interactable 'Dropdownselect'.
    """
    # -------------------- setup --------------------
    __dropdown: Dropdown

    def __init__(self, opts: list[Element], startState: int=0, buttonActive: bool=True, **dpdkwargs) -> None:
        InteractableCore.__init__(self, Rect())
        Togglable.__init__(self, numberOfStates=len(opts)+1, startState=startState, buttonActive=buttonActive)

        self.__innerSetup(opts, **dpdkwargs)

    def __innerSetup(self, inner: list[Element], **kwargs) -> None:
        for nr, el in enumerate(inner):
            isbutton: bool = False
            def hifrombutton():
                nonlocal isbutton
                isbutton = True
            el.set({'buttonCheck':(hifrombutton,[])})
            if isbutton:
                el.set({'quickSubscribeToClick':(self._onCustomTrigger, [lambda _, k=nr+1: k])})

        inner.insert(0, Box.parseFromArgs({}))
        kwargs['inner'] = inner
        self.__dropdown = Dropdown.parseFromArgs(kwargs)

        self.__dropdown.set({'removeTriggerEvent':InputManager.getEvent(InputEvent.LEFTDOWN)})
        self.__dropdown.set({'addGlobalTriggerEvent':self._onclick})

        self.__dropdown.align(self)
        self.__dropdown.alignSize(self)
        
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
                        self.addTriggerEvent(event)
        if not hasTrigger:
            self.addTriggerEvent(InputManager.getEvent(InputEvent.LEFTDOWN))

    # -------------------- getter --------------------

    def getDropdown(self) -> Dropdown:
        return self.__dropdown

    @override
    def getInnerSizing(self, elSize: tuple[int, int], args: dict[str, Any]) -> tuple[int, int]:
        return elSize

    # -------------------- setter --------------------

    def setinner(self, args: dict[str, Any], sets: int=-1, maxDepth: int=-1, skips: list[int]=[0]) -> int:
        return self.__dropdown.set(args, sets, maxDepth, skips)


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


from typing import Any, Callable, Optional, override

from ......utility      import Rect
from ......interaction  import Togglable
from ....element        import Element
from ..interactablecore import InteractableCore
from ..toggle           import Toggle

class MultiselectCore(InteractableCore, Togglable):
    """
    MultiselectCore is the core object of the interactable 'Multiselect'.
    """
    # -------------------- creation --------------------
    __restriction: Callable[[int], int]
    __innerSelectors: list[Toggle]

    def __init__(self, elements: list[Element], startState: int=0x0, restriction: Optional[Callable[[int], int]]=None, buttonActive: bool=True) -> None:
        # init super
        InteractableCore.__init__(self, Rect())
        Togglable.__init__(self, numberOfStates=2**len(elements)-1, startState=startState, buttonActive=buttonActive)
        
        # set basic attributes
        if restriction is None:
            self.__restriction = lambda _: 2**len(elements) - 1
        else:
            self.__restriction = restriction

        # init inner
        self.__innerSetup(elements, startState=startState, buttonActive=buttonActive)

    def __innerSetup(self, elements: list[Element], startState: int=0x0, buttonActive: bool=True) -> None:
        self.__innerSelectors = []
        for nr, el in enumerate(elements):
            istoggle: bool = False
            def hifromtoggle():
                nonlocal istoggle
                istoggle = True
            el.set({'toggleCheck':(hifromtoggle,[])})
            if istoggle:
                el.set({'quickSubscribeToClick':(self.__selectorToggle, [nr])})
                el.set({'buttonActive':buttonActive})
                self.__innerSelectors.append(el)
        if buttonActive:
            self.__applyRestriction()
        else:
            self.setButtonActive(False)

    # -------------------- intern-functionality --------------------
    
    def __selectorToggle(self, selector: int) -> None:
        self._currentState ^= (1 << selector)
        self.__applyRestriction()

    def __applyRestriction(self) -> None:
        restriction: int = self.__restriction(self._currentState)
        for nr, selector in enumerate(self.__innerSelectors):
            selector.set({'setButtonActive':bool(restriction & (1 << nr))})

    # -------------------- additional-getter --------------------

    @override
    def getInnerSizing(self, elSize: tuple[int, int], args: dict[str, Any]) -> tuple[int, int]:
        return elSize

    def getState(self) -> int:
        return self._currentState

    def getSelectorState(self, selector: int) -> bool:
        return bool(self._currentState & (1 << selector))

    # -------------------- active-state --------------------

    @override
    def getButtonActive(self) -> bool:
        return self._buttonActive

    @override
    def setButtonActive(self, buttonActive: bool) -> None:
        self._buttonActive = buttonActive
        if buttonActive:
            self.__applyRestriction()
        else:
            for s in self.__innerSelectors:
                s.set({'setButtonActive':False})

    @override
    def toggleButtonActive(self) -> bool:
        self._buttonActive = not self._buttonActive
        self.setButtonActive(self._buttonActive)
        return self._buttonActive

    # -------------------- subscriptions --------------------

    # MISSING

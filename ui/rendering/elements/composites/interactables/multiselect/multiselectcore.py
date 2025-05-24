from typing import Any, Callable, Optional, override

from ......utility      import Rect, Parsable
from ......interaction  import InputEvent, InputManager, Togglable
from ....element        import Element
from ..interactablecore import InteractableCore
from ...addons          import Stacked
from ..togglewrapper    import Togglewrapper

class MultiselectCore(InteractableCore, Togglable):
    """
    MultiselectCore is the core object of the interactable 'Multiselect'.
    """
    # -------------------- creation --------------------
    __restriction: Callable[[int], int]
    __innerSelectors: list[Togglewrapper]
    __inner: Stacked

    def __init__(self, rect: Rect, *inner: tuple[Element, float], alignVertical: bool=True, offset: int=0,
                 startState: int=0x0, restriction: Optional[Callable[[int], int]]=None, buttonActive: bool=True, args: dict[str, Any]={}) -> None:
        # set basic attributes
        Togglable.__init__(self, numberOfStates=2**len(inner)-1, startState=startState, buttonActive=buttonActive)
        if restriction is None:
            self.__restriction = lambda _: 2**len(inner) - 1
        else:
            self.__restriction = restriction

        # init inner
        self.__inner = Stacked(rect, rect, *self.__innerSetup(*inner, startState=startState, buttonActive=buttonActive, **args), alignVertical=alignVertical, offset=offset)

        # init super
        InteractableCore.__init__(self, self.__inner.getRect())
        
        # align inner
        self.__inner.align(self)
        self.__inner.alignSize(self)

    def __innerSetup(self, *inner: tuple[Element, float], startState: int=0x0, buttonActive: bool=True, **kwargs) -> list[tuple[Togglewrapper, float]]:
        self.__innerSelectors = []
        sizedSelectors: list[tuple[Togglewrapper, float]] = []
        for nr, el in enumerate(inner):
            newSelector: Togglewrapper = Togglewrapper(el[0], startState=startState & (1 << nr), buttonActive=buttonActive)
            newSelector.set({'quickSubscribeToClick':(self.__selectorToggle, [nr])})
            sizedSelectors.append((newSelector, el[1]))
            self.__innerSelectors.append(newSelector)
        if buttonActive:
            self.__applyRestriction()
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
                case 'globaltrigger' | 'gtrigger' | 'global':
                    hasTrigger = True
                    for v in Parsable.parseList(value):
                        event: str = ''
                        if v.lower() == 'click':
                            event = InputManager.getEvent(InputEvent.LEFTDOWN)
                        else:
                            event = InputManager.getEvent(InputEvent.fromStr(v))
                        for s in self.__innerSelectors:
                            s.set({'addGlobalTriggerEvent':event})
        if not hasTrigger:
            event = InputManager.getEvent(InputEvent.LEFTDOWN)
            for s in self.__innerSelectors:
                s.set({'addTriggerEvent':event})
        return sizedSelectors


    # -------------------- intern-functionality --------------------
    
    def __selectorToggle(self, selector: int) -> None:
        self._currentState ^= (1 << selector)
        self.__applyRestriction()

    def __applyRestriction(self) -> None:
        restriction: int = self.__restriction(self._currentState)
        for nr, selector in enumerate(self.__innerSelectors):
            selector.set({'setButtonActive':bool(restriction & (1 << nr))})

    # -------------------- additional-getter --------------------

    def getInner(self) -> Stacked:
        return self.__inner

    @override
    def getInnerSizing(self, elSize: tuple[int, int], args: dict[str, Any]) -> tuple[int, int]:
        return self.__inner.getInnerSizing(elSize, args)

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

    # -------------------- setter --------------------

    @override
    def addTriggerEvent(self, event: str) -> bool:
        for s in self.__innerSelectors:
            s.set({'addTriggerEvent':event})
        return True

    @override
    def removeTriggerEvent(self, event: str) -> bool:
        for s in self.__innerSelectors:
            s.set({'removeTriggerEvent':event})
        return True

    @override
    def addGlobalTriggerEvent(self, event: str) -> bool:
        for s in self.__innerSelectors:
            s.set({'addGlobalTriggerEvent':event})
        return True

    @override
    def removeGlobalTriggerEvent(self, event: str) -> bool:
        for s in self.__innerSelectors:
            s.set({'removeGlobalTriggerEvent':event})
        return True

    # -------------------- subscriptions --------------------

    def subscribeToSelectorSelect(self, selector: int, callback: str) -> bool:
        """
        subscribeToSelectorSelect subscribes a Callback to the select-event of the selector
        with the given index.

        Args:
            selector (int): the index of the selector to subscribe to
            callback (str): the id of the callback to subscribe to

        Returns (bool): returns if the subscription was successful
        """
        if 0 <= selector < len(self.__innerSelectors):
            self.__innerSelectors[selector].set({'subscribeToToggleState':(1, callback)})
            return True
        return False

    def unsubscribeToSelectorSelect(self, selector: int, callback: str) -> bool:
        """
        unsubscribeToSelectorSelect unsubscribes a Callback to the select-event of the selector
        with the given index.

        Args:
            selector (int): the index of the selector to unsubscribe from
            callback (str): the id of the callback to unsubscribe from

        Returns (bool): returns if the unsubscription was successful
        """
        if 0 <= selector < len(self.__innerSelectors):
            self.__innerSelectors[selector].set({'unsubscribeToToggleState':(1, callback)})
            return True
        return False

    def quicksubscribeToSelectorSelect(self, selector: int, f: Callable, *args: Any) -> bool:
        """
        quicksubscribeToSelectorSelect subscribes a function to the select-event of the selector
        with the given index.

        Args:
            selector (int): the index of the selector to unsubscribe from
            f (Callable)  : the function to subscribe to the selector select event
            *args (Any)   : the arguments of the function

        Returns (bool): returns if the subscription was successful
        """
        if 0 <= selector < len(self.__innerSelectors):
            self.__innerSelectors[selector].set({'quicksubscribeToToggleState':(1, f, list(args))})
            return True
        return False

    def subscribeToSelectorDeselect(self, selector: int, callback: str) -> bool:
        """
        subscribeToSelectorDeselect subscribes a Callback to the select-event of the selector
        with the given index.

        Args:
            selector (int): the index of the selector to subscribe to
            callback (str): the id of the callback to subscribe to

        Returns (bool): returns if the subscription was successful
        """
        if 0 <= selector < len(self.__innerSelectors):
            self.__innerSelectors[selector].set({'subscribeToToggleState':(0, callback)})
            return True
        return False

    def unsubscribeToSelectorDeselect(self, selector: int, callback: str) -> bool:
        """
        unsubscribeToSelectorDeselect unsubscribes a Callback to the select-event of the selector
        with the given index.

        Args:
            selector (int): the index of the selector to unsubscribe from
            callback (str): the id of the callback to unsubscribe from

        Returns (bool): returns if the unsubscription was successful
        """
        if 0 <= selector < len(self.__innerSelectors):
            self.__innerSelectors[selector].set({'unsubscribeToToggleState':(0, callback)})
            return True
        return False

    def quicksubscribeToSelectorDeselect(self, selector: int, f: Callable, *args: Any) -> bool:
        """
        quicksubscribeToSelectorDeselect subscribes a function to the select-event of the selector
        with the given index.

        Args:
            selector (int): the index of the selector to unsubscribe from
            f (Callable)  : the function to subscribe to the selector select event
            *args (Any)   : the arguments of the function

        Returns (bool): returns if the subscription was successful
        """
        if 0 <= selector < len(self.__innerSelectors):
            self.__innerSelectors[selector].set({'quicksubscribeToToggleState':(0, f, list(args))})
            return True
        return False

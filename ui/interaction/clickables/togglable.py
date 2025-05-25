from abc import ABC
from typing import Any, Callable, override

from ..event        import EventManager
from .clickable     import Clickable

class Togglable(Clickable, ABC):

    __toggleEvents: dict[int, str]
    _numberOfStates: int
    _currentState: int

    def __init__(self, numberOfStates: int=2, startState: int=0, buttonActive: bool=True) -> None:
        Clickable.__init__(self, buttonActive)
        
        self._numberOfStates    = max(2, numberOfStates)
        self._currentState      = max(0, min(self._numberOfStates-1, startState))

        self.__toggleEvents = {}

    # -------------------- getter --------------------

    def getNumberOfToggleStates(self) -> int:
        return self._numberOfStates

    def getCurrentToggleState(self) -> int:
        return self._currentState

    def getStateEvent(self, state: int) -> str:
        if state not in self.__toggleEvents:
            self.__toggleEvents[state] = EventManager.createEvent()
        return self.__toggleEvents[state]

    # -------------------- triggering --------------------

    def __onStateTrigger(self) -> None:
        """
        onStateTrigger triggers the Event of the currentState
        """
        EventManager.triggerEvent(self.getStateEvent(self._currentState))
    
    @override
    def _onTrigger(self) -> bool:
        """
        onTrigger gets called when the Toggle is triggered.
        """
        if self._buttonActive:
            super()._onTrigger()
            self._currentState = (self._currentState + 1) % self._numberOfStates
            self.__onStateTrigger()
            return True
        return False

    def _onCustomTrigger(self, switchTo: Callable[[int], int]) -> bool:
        """
        onCustomTrigger gets called internally when switching
        to a custom new state.
        """
        if self._buttonActive:
            super()._onTrigger()
            self._currentState = max(0, min(self._numberOfStates-1, switchTo(self._currentState)))
            self.__onStateTrigger()
            return True
        return False
    
    # -------------------- subscriptions --------------------

    def subscribeToToggleState(self, state: int, callback: str) -> bool:
        """
        subscribeToToggleState subscribes a Callback to the triggerEvent of the
        given toggleState of the Toggle.

        Args:
            state    (int): the toggleState the Callback should be subscribed to
            callback (str): the id of the callback to subscribe to toggleState

        Returns (bool): returns if the subscription was successful
        """
        if state >= 0 and state < self._numberOfStates:
            return EventManager.subscribeToEvent(self.getStateEvent(state), callback)
        return False

    def unsubscribeToToggleState(self, state: int, callback: str) -> bool:
        """
        unsubscribeToToggleState unsubscribes a callback (by id) from the Event of the
        toggle being in a given state.

        Args:
            state    (int): the toggleState the Callback should be unsubscribed from
            callback (str): the id of the callback to unsubscribe

        Returns (bool): if the unsubscription was successful
        """
        if state >= 0 and state < self._numberOfStates:
            return EventManager.unsubscribeToEvent(self.getStateEvent(state), callback)
        return False

    def quickSubscribeToToggleState(self, state: int, f: Callable, *args: Any) -> tuple[str, bool]:
        """
        quickSubscribeToToggleState takes a function and its arguments, creates
        a Callback and subscribes to the Event of the toggle being in a given state.

        Args:
            state (int)      : the toggleState the function should subscribe to
            f     (Callable) : the function to use as callback
            args  (list[Any]): the arguments to use as callback

        Returns (tuple[str, bool]): 1. the id of the newly created Callback
                                    2. if the callback was successfully subscribed
        """
        newCallback: str = EventManager.createCallback(f, *args)
        return (newCallback, self.subscribeToToggleState(state, newCallback))

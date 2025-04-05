from abc import ABC
from typing import Any, Callable, override

from ..event        import EventManager
from .clickable     import Clickable

class Togglable(Clickable, ABC):

    __toggleEvents: list[str]
    _numberOfStates: int
    _currentState: int

    def __init__(self, numberOfStates: int=2, startState: int=0, buttonActive: bool=True) -> None:
        Clickable.__init__(self, buttonActive)
        
        self._numberOfStates    = max(2, numberOfStates)
        self._currentState      = max(0, min(self._numberOfStates-1, startState))

        self.__toggleEvents = [EventManager.createEvent() for _ in range(self._numberOfStates)]

    # -------------------- getter --------------------

    def getNumberOfToggleStates(self) -> int:
        return self._numberOfStates

    def getCurrentToggleState(self) -> int:
        return self._currentState

    # -------------------- triggering --------------------

    def __onStateTrigger(self) -> None:
        """
        onStateTrigger triggers the Event of the currentState and cycles to
        the next one.
        """
        self._currentState = (self._currentState + 1) % self._numberOfStates
        EventManager.triggerEvent(self.__toggleEvents[self._currentState])
    
    @override
    def _onTrigger(self) -> None:
        """
        onTrigger gets called when the Toggle is triggered.
        """
        EventManager.triggerEvent(self._onclick)
        self.__onStateTrigger()
    
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
            return EventManager.subscribeToEvent(self.__toggleEvents[state], callback)
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
            return EventManager.unsubscribeToEvent(self.__toggleEvents[state], callback)
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

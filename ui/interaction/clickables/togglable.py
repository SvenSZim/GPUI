from abc import ABC
from typing import Any, Callable, override

from ..event        import EventManager
from .clickable     import Clickable

class Togglable(Clickable, ABC):

    __toggleEvents: list[str]
    _numberOfStates: int
    _currentState: int

    def __init__(self, numberOfStates: int=2, startState: int=0, toggleActive: bool=True) -> None:
        Clickable.__init__(self, toggleActive)
        
        self._numberOfStates    = max(2, numberOfStates)
        self._currentState      = max(0, min(self._numberOfStates-1, startState))

        self.__toggleEvents = [EventManager.createEvent() for _ in range(self._numberOfStates)]

    def getNumberOfToggleStates(self) -> int:
        return self._numberOfStates

    def getCurrentToggleState(self) -> int:
        return self._currentState

    def __onStateTrigger(self) -> None:
        """
        onStateTrigger triggers the Event of the currentState and cycles to
        the next one.
        """
        EventManager.triggerEvent(self.__toggleEvents[self._currentState])
        self._currentState = (self._currentState + 1) % self._numberOfStates
    
    @override
    def _onTrigger(self) -> None:
        """
        onTrigger gets called when the Toggle is triggered.
        """
        EventManager.triggerEvent(self._onclick)
        self.__onStateTrigger()

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


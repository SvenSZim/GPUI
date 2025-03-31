from typing import Any, Callable, override

from .....interaction import EventManager, InputManager, InputEvent
from ....utility import Rect, Clickable
from ..atomcore import AtomCore

class ToggleCore(AtomCore, Clickable):

    __toggleEvents: list[str]
    __numberOfStates: int
    __currentState: int

    def __init__(self, rect: Rect, numberOfStates: int=2, startState: int=0, toggleActive: bool=True) -> None:
        AtomCore.__init__(self, rect)
        Clickable.__init__(self, toggleActive)
        
        self.__numberOfStates    = max(2, numberOfStates)
        self.__currentState      = max(0, min(self.__numberOfStates-1, startState))

        self.__toggleEvents = [EventManager.createEvent() for _ in range(self.__numberOfStates)]

        EventManager.subscribeToEvent(InputManager.getEvent(InputEvent.MOUSEBUTTONDOWN), ToggleCore.activeTrigger, self)

    def getNumberOfToggleStates(self) -> int:
        return self.__numberOfStates

    def getCurrentToggleState(self) -> int:
        return self.__currentState

    def __onStateTrigger(self) -> None:
        """
        onStateTrigger triggers the Event of the currentState and cycles to
        the next one.
        """
        EventManager.triggerEvent(self.__toggleEvents[self.__currentState])
        self.__currentState = (self.__currentState + 1) % self.__numberOfStates
    
    @override
    def _onTrigger(self) -> None:
        """
        onTrigger gets called when the Toggle is triggered.
        """
        EventManager.triggerEvent(self._onclick)
        self.__onStateTrigger()

    def subscribeToToggleState(self, state: int, f: Callable, *args: Any) -> bool:
        """
        subscribeToToggleState subscribes a Callback to the triggerEvent of the
        given toggleState of the Toggle.

        Args:
            state (int): the toggleState the Callback should be subscribed to
            f (Callable): the function that should be subscribed
            *args (Any): the potential arguments the function needs

        Returns (bool): returns if the subscription was successful
        """
        if state >= 0 and state < self.__numberOfStates:
            return EventManager.subscribeToEvent(self.__toggleEvents[state], f, *args)
        return False


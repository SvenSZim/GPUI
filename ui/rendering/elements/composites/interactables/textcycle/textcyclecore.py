
from typing import Any, Callable
from ......utility      import Rect
from ......interaction  import Togglable
from ..interactablecore import InteractableCore

class TextCycleCore(InteractableCore, Togglable):
    """
    TextCycleCore is the core object of the interactable 'TextCycle'.
    """
    def __init__(self, rect: Rect, numberOfStates: int, startState: int=0, buttonActive: bool=True) -> None:
        InteractableCore.__init__(self, rect)
        Togglable.__init__(self, numberOfStates=numberOfStates, startState=startState, buttonActive=buttonActive)

    # -------------------- subscriptions --------------------

    def subscribeToState(self, state: int, callback: str) -> bool:
        """
        subscribeToState subscribes a Callback to the textcycle being selected.
        
        Args:
            state    (int): the state to subscribe the callback to
            callback (str): the id of the callback to subscribe to the selection

        Returns (bool): returns if the subscription was successful
        """
        return self.subscribeToToggleState(state, callback)

    def unsubscribeToState(self, state: int, callback: str) -> bool:
        """
        unsubscribeToState unsubscribes a callback (by id) from the textcycle being selected
        
        Args:
            state    (int): the state to unsubscribe the callback from
            callback (str): the id of the callback to unsubscribe

        Returns (bool): if the unsubscription was successful
        """
        return self.unsubscribeToToggleState(state, callback)

    def quickSubscribeToState(self, state: int, f: Callable, *args: Any) -> tuple[str, bool]:
        """
        quickSubscribeToToggleState takes a function and its arguments, creates
        a Callback and subscribes to the textcycle being selected.

        Args:
            state (int)      : the state to quick subscribe to
            f     (Callable) : the function to use as callback
            args  (list[Any]): the arguments to use as callback

        Returns (tuple[str, bool]): 1. the id of the newly created Callback
                                    2. if the callback was successfully subscribed
        """
        return self.quickSubscribeToToggleState(state, f, *args)



from typing import Any, Callable
from ......utility      import Rect
from ......interaction  import Togglable
from ..interactablecore import InteractableCore

class CheckboxCore(InteractableCore, Togglable):
    """
    CheckboxCore is the core object of the interactable 'Checkbox'.
    """
    def __init__(self, rect: Rect, startState: bool=False, buttonActive: bool=True) -> None:
        InteractableCore.__init__(self, rect)
        Togglable.__init__(self, numberOfStates=2, startState=int(startState), buttonActive=buttonActive)

    # -------------------- subscriptions --------------------

    def subscribeToSelect(self, callback: str) -> bool:
        """
        subscribeToSelect subscribes a Callback to the checkbox being selected.
        
        Args:
            callback (str): the id of the callback to subscribe to the selection

        Returns (bool): returns if the subscription was successful
        """
        return self.subscribeToToggleState(1, callback)

    def unsubscribeToSelect(self, callback: str) -> bool:
        """
        unsubscribeToSelect unsubscribes a callback (by id) from the checkbox being selected
        
        Args:
            callback (str): the id of the callback to unsubscribe

        Returns (bool): if the unsubscription was successful
        """
        return self.unsubscribeToToggleState(1, callback)

    def quickSubscribeToSelect(self, f: Callable, *args: Any) -> tuple[str, bool]:
        """
        quickSubscribeToSelect takes a function and its arguments, creates
        a Callback and subscribes to the checkbox being selected.

        Args:
            f     (Callable) : the function to use as callback
            args  (list[Any]): the arguments to use as callback

        Returns (tuple[str, bool]): 1. the id of the newly created Callback
                                    2. if the callback was successfully subscribed
        """
        return self.quickSubscribeToToggleState(1, f, *args)

    def subscribeToDeselect(self, callback: str) -> bool:
        """
        subscribeToDeselect subscribes a Callback to the checkbox being deselected.
        
        Args:
            callback (str): the id of the callback to subscribe to the deselection

        Returns (bool): returns if the subscription was successful
        """
        return self.subscribeToToggleState(0, callback)

    def unsubscribeToDeselect(self, callback: str) -> bool:
        """
        unsubscribeToDeselect unsubscribes a callback (by id) from the checkbox being deselected
        
        Args:
            callback (str): the id of the callback to unsubscribe

        Returns (bool): if the unsubscription was successful
        """
        return self.unsubscribeToToggleState(0, callback)

    def quickSubscribeToDeselect(self, f: Callable, *args: Any) -> tuple[str, bool]:
        """
        quickSubscribeToDeselect takes a function and its arguments, creates
        a Callback and subscribes to the checkbox being deselected.

        Args:
            f     (Callable) : the function to use as callback
            args  (list[Any]): the arguments to use as callback

        Returns (tuple[str, bool]): 1. the id of the newly created Callback
                                    2. if the callback was successfully subscribed
        """
        return self.quickSubscribeToToggleState(0, f, *args)


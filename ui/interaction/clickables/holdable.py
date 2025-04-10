from abc import ABC
from typing import Any, Callable, override

from ..event        import EventManager
from ..inputmanager import InputManager, InputEvent
from .clickable     import Clickable

class Holdable(Clickable, ABC):

    _activeReleaseCallback: str
    _onHoldTriggerCallback: str

    _onhold: str
    _isPressed: bool
    
    def __init__(self, buttonActive: bool=True) -> None:
        Clickable.__init__(self, buttonActive)

        self._activeReleaseCallback = EventManager.createCallback(self._onRelease)
        self._onHoldTriggerCallback = EventManager.createCallback(self._onHoldTrigger)
        self._onhold = EventManager.createEvent()

        self._isPressed = False

    # -------------------- getter --------------------

    def isPressed(self) -> bool:
        """
        isPressed returns if the button is currently being pressed.
        """
        return self._isPressed

    # -------------------- triggering --------------------

    def _onRelease(self) -> None:
        """
        onRelease gets called when the Button is released.
        """
        EventManager.unsubscribeToEvent(InputManager.getEvent(InputEvent.LEFTUP), self._activeReleaseCallback)
        EventManager.unsubscribeToEvent(InputManager.getEvent(InputEvent.UPDATE), self._onHoldTriggerCallback)

        self._isPressed = False

    def _onHoldTrigger(self) -> None:
        EventManager.triggerEvent(self._onhold)

    @override
    def _onTrigger(self) -> None:
        """
        onTrigger gets called when the Button is triggered.
        """
        super()._onTrigger()
        EventManager.subscribeToEvent(InputManager.getEvent(InputEvent.LEFTUP), self._activeReleaseCallback)
        EventManager.subscribeToEvent(InputManager.getEvent(InputEvent.UPDATE), self._onHoldTriggerCallback)

        self._isPressed = True

    # -------------------- subscriptions --------------------

    def subscribeToHold(self, callback: str) -> bool:
        """
        subscribeToHold subscribes a Callback to the Event of the button
        getting pressed down.

        Args:
            callback (str): the id of the callback to subscribe to the click

        Returns (bool): returns if the subscription was successful
        """
        return EventManager.subscribeToEvent(self._onhold, callback)
    
    def unsubscribeToHold(self, callback: str) -> bool:
        """
        unsubscribeToHold unsubscribes a callback (by id) from the Event of the
        button getting pressed down.

        Args:
            callback (str): the id of the callback to unsubscribe

        Returns (bool): if the unsubscription was successful
        """
        return EventManager.unsubscribeToEvent(self._onhold, callback)

    def quickSubscribeToHold(self, f: Callable, *args: Any) -> tuple[str, bool]:
        """
        quickSubscribeToHold takes a function and its arguments, creates
        a Callback and subscribes to the Event of the button getting pressed down.

        Args:
            f     (Callable) : the function to use as callback
            args  (list[Any]): the arguments to use as callback

        Returns (tuple[str, bool]): 1. the id of the newly created Callback
                                    2. if the callback was successfully subscribed
        """
        newCallback: str = EventManager.createCallback(f, *args)
        return (newCallback, EventManager.subscribeToEvent(self._onhold, newCallback))

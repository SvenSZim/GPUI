from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Callable

from ...utility     import iRect, Rect
from ..event        import EventManager
from ..inputmanager import InputManager

class Clickable(iRect, ABC):

    _activeTriggerCallback: str
    _passiveTriggerCallback: str

    _onclick: str
    _buttonActive: bool

    def __init__(self, buttonActive: bool=True) -> None:
        self._buttonActive = buttonActive
        self._onclick = EventManager.createEvent()

        self._activeTriggerCallback = EventManager.createCallback(self.activeTrigger)
        self._passiveTriggerCallback = EventManager.createCallback(self.passiveTrigger)

    # -------------------- active-state --------------------

    def getButtonActive(self) -> bool:
        """
        getButtonActive returns the active-state of the Button

        Returns (bool): active-state of the Button
        """
        return self._buttonActive

    def setButtonActive(self, buttonActive: bool) -> None:
        """
        setButtonActive sets the active-state of the Button

        Args:
            buttonActive (bool): new active-state of the Button
        """
        self._buttonActive = buttonActive

    def toggleButtonActive(self) -> bool:
        """
        toggleButtonActive toggles the active-state of the Button

        Returns (bool): the new active-state of the Button
        """
        self._buttonActive = not self._buttonActive
        return self._buttonActive

    # -------------------- triggering --------------------

    def _onTrigger(self) -> None:
        """
        onTrigger gets called when the Button is triggered.
        """
        EventManager.triggerEvent(self._onclick)

    def activeTrigger(self) -> None:
        """
        activeTrigger is the default function to call when trying to trigger the
        Button. It checks if the mouse is inside the bounds of the Button before triggering.
        """
        if Rect(self.getPosition(), self.getSize()).collidepoint(InputManager.getMousePosition()):
            if self._buttonActive:
                self._onTrigger()

    def passiveTrigger(self) -> None:
        """
        passiveTrigger is the global alternative of activeTrigger which does not
        check for the mouse to be inside the bounds. (useful for using keys to trigger buttons)
        """
        if self._buttonActive:
            self._onTrigger()

    # -------------------- managing-trigger-events --------------------

    def addTriggerEvent(self, event: str) -> bool:
        """
        addTriggerEvent adds a event which activates the activeTrigger.
        """
        return EventManager.subscribeToEvent(event, self._activeTriggerCallback)

    def removeTriggerEvent(self, event: str) -> bool:
        """
        removeTriggerEvent removes a event which activates the activeTrigger.
        """
        return EventManager.unsubscribeToEvent(event, self._activeTriggerCallback)
    
    def addGlobalTriggerEvent(self, event: str) -> bool:
        """
        addGlobalTriggerEvent adds a event which immediatly triggers the button.
        """
        return EventManager.subscribeToEvent(event, self._passiveTriggerCallback)

    def removeGlobalTriggerEvent(self, event: str) -> bool:
        """
        removeGlobalTriggerEvent removes a event which immediatly triggers the button.
        """
        return EventManager.unsubscribeToEvent(event, self._passiveTriggerCallback)
    
    # -------------------- subscriptions --------------------

    def subscribeToClick(self, callback: str) -> bool:
        """
        subscribeToClick subscribes a Callback to the Event of the object
        getting clicked.

        Args:
            callback (str): the id of the callback to subscribe to the click

        Returns (bool): returns if the subscription was successful
        """
        return EventManager.subscribeToEvent(self._onclick, callback)
    
    def unsubscribeToClick(self, callback: str) -> bool:
        """
        unsubscribeToClick unsubscribes a callback (by id) from the Event of the
        object getting clicked.

        Args:
            callback (str): the id of the callback to unsubscribe

        Returns (bool): if the unsubscription was successful
        """
        return EventManager.unsubscribeToEvent(self._onclick, callback)

    def quickSubscribeToClick(self, f: Callable, *args: Any) -> tuple[str, bool]:
        """
        quickSubscribeToClick takes a function and its arguments, creates
        a Callback and subscribes to the Event of the object getting clicked.

        Args:
            f     (Callable) : the function to use as callback
            args  (list[Any]): the arguments to use as callback

        Returns (tuple[str, bool]): 1. the id of the newly created Callback
                                    2. if the callback was successfully subscribed
        """
        newCallback: str = EventManager.createCallback(f, *args)
        return (newCallback, EventManager.subscribeToEvent(self._onclick, newCallback))

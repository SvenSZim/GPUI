from abc import ABC
from typing import Any, Callable

from ...interaction import EventManager, InputManager
from ..utility      import iRect, Rect

class Clickable(iRect, ABC):

    _onclick: str
    _clickableActive: bool

    def __init__(self, clickableActive: bool=True) -> None:
        self._clickableActive = clickableActive
        self._onclick = EventManager.createEvent()

    # -------------------- active-state --------------------

    def getClickableActive(self) -> bool:
        """
        getClickableActive returns the active-state of the Clickable

        Returns (bool): active-state of the Clickable
        """
        return self._clickableActive

    def setClickableActive(self, clickableActive: bool) -> None:
        """
        setClickableActive sets the active-state of the Clickable

        Args:
            clickableActive (bool): new active-state of the Clickable
        """
        self._clickableActive = clickableActive

    def toggleClickableActive(self) -> bool:
        """
        toggleClickableActive toggles the active-state of the Clickable

        Returns (bool): the new active-state of the Clickable
        """
        self._clickableActive = not self._clickableActive
        return self._clickableActive

    # -------------------- triggering --------------------

    def _onTrigger(self) -> None:
        """
        onTrigger gets called when the Clickable is triggered.
        """
        if self._clickableActive:
            EventManager.triggerEvent(self._onclick)

    def activeTrigger(self) -> None:
        """
        activeTrigger is the default function to call when trying to trigger the
        Clickable. It checks if the mouse is inside the bounds of the Clickable before triggering.
        """
        if Rect(self.getPosition(), self.getSize()).collidepoint(InputManager.getMousePosition()):
            self._onTrigger()

    def passiveTrigger(self) -> None:
        """
        passiveTrigger is the global alternative of activeTrigger which does not
        check for the mouse to be inside the bounds. (useful for using keys to trigger buttons)
        """
        self._onTrigger()
    

    def addTriggerEvent(self, event: str) -> bool:
        """
        addTriggerEvent adds a event which activates the activeTrigger.
        """
        return EventManager.subscribeToEvent(event, self.activeTrigger)
    
    def addGlobalTriggerEvent(self, event: str) -> bool:
        """
        addGlobalTriggerEvent adds a event which immediatly triggers the toggle.
        """
        return EventManager.subscribeToEvent(event, self.passiveTrigger)
    
    # -------------------- subscriptions --------------------

    def subscribeToClick(self, f: Callable, *args: Any) -> bool:
        """
        subscribeToClick subscribes a Callback to the Event of the object
        getting clicked.

        Args:
            f (Callable): the function that should be subscribed
            *args (Any): the potential arguments the function needs

        Returns (bool): returns if the subscription was successful
        """
        return EventManager.subscribeToEvent(self._onclick, f, *args)



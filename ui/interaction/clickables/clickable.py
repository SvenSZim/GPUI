from abc import ABC

from ...utility     import iRect, Rect
from ..event        import EventManager
from ..inputmanager import InputManager, InputEvent

class Clickable(iRect, ABC):

    _onclick: str
    _clickableActive: bool

    def __init__(self, clickableActive: bool=True) -> None:
        self._clickableActive = clickableActive
        self._onclick = EventManager.createEvent()

        EventManager.quickSubscribe(InputManager.getEvent(InputEvent.LEFTDOWN), self.activeTrigger)

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
        return EventManager.quickSubscribe(event, self.activeTrigger)[1]
    
    def addGlobalTriggerEvent(self, event: str) -> bool:
        """
        addGlobalTriggerEvent adds a event which immediatly triggers the toggle.
        """
        return EventManager.quickSubscribe(event, self.passiveTrigger)[1]
    
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



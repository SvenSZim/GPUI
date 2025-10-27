from abc import ABC
from typing import Any, Callable

from ...utility     import iRect, Rect
from ..event        import EventManager
from ..inputmanager import InputManager

class Clickable(iRect, ABC):
    """Abstract base class for clickable UI elements with event handling.

    Provides core functionality for UI elements that can be clicked or triggered:
    - Click detection with mouse position checking
    - Active and passive trigger modes
    - Event subscription system
    - Priority-based event handling
    - Enable/disable functionality

    Features:
    - Supports both mouse and keyboard triggers
    - Maintains active/inactive state
    - Handles event subscriptions
    - Supports priority levels
    - Provides collision detection

    Attributes:
        _activeTriggerCallback (str): ID for mouse-position-checked trigger
        _passiveTriggerCallback (str): ID for unchecked trigger
        _onclick (str): Event ID for click handling
        _buttonActive (bool): Current active state
    """

    _activeTriggerCallback: str
    _passiveTriggerCallback: str
    _onclick: str
    _buttonActive: bool

    def __init__(self, buttonActive: bool=True) -> None:
        """Initialize a new clickable element.

        Args:
            buttonActive (bool, optional): Initial active state. Defaults to True.

        Raises:
            TypeError: If buttonActive is not a boolean
        """
        if not isinstance(buttonActive, bool):
            raise TypeError(f'buttonActive must be a boolean, got {type(buttonActive)}')

        self._buttonActive = buttonActive
        self._onclick = EventManager.createEvent()
        
        # Create bound callbacks with proper type checking
        if not hasattr(self, 'activeTrigger') or not callable(getattr(self, 'activeTrigger')):
            raise TypeError('Class must implement activeTrigger method')
        if not hasattr(self, 'passiveTrigger') or not callable(getattr(self, 'passiveTrigger')):
            raise TypeError('Class must implement passiveTrigger method')
            
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

    # -------------------- change-priority --------------------

    def setPriority(self, priority: int) -> None:
        """Set the execution priority for both trigger callbacks.

        Updates priority for both active (mouse-checked) and passive triggers.
        Higher priority callbacks execute before lower priority ones.

        Args:
            priority (int): New priority level (-1000 to 1000)

        Raises:
            TypeError: If priority is not an integer
            ValueError: If priority is outside valid range
        """
        if not isinstance(priority, int):
            raise TypeError(f'priority must be an integer, got {type(priority)}')
        if not -1000 <= priority <= 1000:
            raise ValueError(f'priority must be between -1000 and 1000, got {priority}')

        EventManager.setPriority(self._passiveTriggerCallback, priority)
        EventManager.setPriority(self._activeTriggerCallback, priority)

    # -------------------- triggering --------------------

    def _onTrigger(self) -> bool:
        """
        onTrigger gets called when the Button is triggered.
        """
        if self._buttonActive:
            EventManager.triggerEvent(self._onclick)
            return True
        return False

    def activeTrigger(self) -> bool:
        """Trigger the clickable only if mouse is within bounds.

        Performs mouse position collision detection before triggering.
        Used for normal mouse-click handling.

        Returns:
            bool: True if triggered and active, False otherwise

        Raises:
            RuntimeError: If position or size getters fail
        """
        try:
            clickBounds = Rect(self.getPosition(), self.getSize())
            mousePos = InputManager.getMousePosition()
            if clickBounds.collidepoint(mousePos):
                return self._onTrigger()
            return False
        except Exception as e:
            raise RuntimeError(f'Failed to check click bounds: {str(e)}')

    def passiveTrigger(self) -> None:
        """Trigger the clickable without position checking.

        Global trigger used for keyboard shortcuts or programmatic
        activation without mouse position requirements.

        Note:
            Does not return trigger result to maintain compatibility
            with existing event system.
        """
        self._onTrigger()

    # -------------------- managing-trigger-events --------------------

    def addTriggerEvent(self, event: str) -> bool:
        """Subscribe to an event that triggers with mouse position checking.

        Args:
            event (str): Event identifier to subscribe to

        Returns:
            bool: True if subscription successful, False otherwise

        Raises:
            TypeError: If event is not a string
            ValueError: If event is empty
        """
        if not isinstance(event, str):
            raise TypeError(f'event must be a string, got {type(event)}')
        if not event:
            raise ValueError('event identifier cannot be empty')
        return EventManager.subscribeToEvent(event, self._activeTriggerCallback)

    def removeTriggerEvent(self, event: str) -> bool:
        """Remove a mouse-position-checked trigger event subscription.

        Args:
            event (str): Event identifier to unsubscribe from

        Returns:
            bool: True if unsubscription successful, False otherwise

        Raises:
            TypeError: If event is not a string
            ValueError: If event is empty
        """
        if not isinstance(event, str):
            raise TypeError(f'event must be a string, got {type(event)}')
        if not event:
            raise ValueError('event identifier cannot be empty')
        return EventManager.unsubscribeToEvent(event, self._activeTriggerCallback)
    
    def addGlobalTriggerEvent(self, event: str) -> bool:
        """Subscribe to an event that triggers immediately without checks.

        Args:
            event (str): Event identifier to subscribe to

        Returns:
            bool: True if subscription successful, False otherwise

        Raises:
            TypeError: If event is not a string
            ValueError: If event is empty
        """
        if not isinstance(event, str):
            raise TypeError(f'event must be a string, got {type(event)}')
        if not event:
            raise ValueError('event identifier cannot be empty')
        return EventManager.subscribeToEvent(event, self._passiveTriggerCallback)

    def removeGlobalTriggerEvent(self, event: str) -> bool:
        """Remove an immediate trigger event subscription.

        Args:
            event (str): Event identifier to unsubscribe from

        Returns:
            bool: True if unsubscription successful, False otherwise

        Raises:
            TypeError: If event is not a string
            ValueError: If event is empty
        """
        if not isinstance(event, str):
            raise TypeError(f'event must be a string, got {type(event)}')
        if not event:
            raise ValueError('event identifier cannot be empty')
        return EventManager.unsubscribeToEvent(event, self._passiveTriggerCallback)
    
    # -------------------- subscriptions --------------------

    def subscribeToClick(self, callback: str) -> bool:
        """Subscribe a callback to handle click events.

        Args:
            callback (str): Callback identifier to subscribe

        Returns:
            bool: True if subscription successful, False otherwise

        Raises:
            TypeError: If callback is not a string
            ValueError: If callback is empty
        """
        if not isinstance(callback, str):
            raise TypeError(f'callback must be a string, got {type(callback)}')
        if not callback:
            raise ValueError('callback identifier cannot be empty')
        return EventManager.subscribeToEvent(self._onclick, callback)
    
    def unsubscribeToClick(self, callback: str) -> bool:
        """Remove a click event callback subscription.

        Args:
            callback (str): Callback identifier to unsubscribe

        Returns:
            bool: True if unsubscription successful, False otherwise

        Raises:
            TypeError: If callback is not a string
            ValueError: If callback is empty
        """
        if not isinstance(callback, str):
            raise TypeError(f'callback must be a string, got {type(callback)}')
        if not callback:
            raise ValueError('callback identifier cannot be empty')
        return EventManager.unsubscribeToEvent(self._onclick, callback)

    def quickSubscribeToClick(self, f: Callable, *args: Any) -> tuple[str, bool]:
        """Create and subscribe a new callback function for click events.

        Convenience method that creates a callback from a function and its
        arguments, then subscribes it to handle click events.

        Args:
            f: Function to call when clicked
            *args: Arguments to pass to the function

        Returns:
            tuple: (callback_id, subscription_success)
                callback_id: Identifier for the created callback
                subscription_success: True if subscription successful

        Raises:
            TypeError: If f is not callable
        """
        if not callable(f):
            raise TypeError(f'f must be callable, got {type(f)}')
        
        newCallback: str = EventManager.createCallback(f, *args)
        success = EventManager.subscribeToEvent(self._onclick, newCallback)
        if not success:
            # Clean up callback if subscription failed
            EventManager.removeCallback(newCallback)
        return (newCallback, success)

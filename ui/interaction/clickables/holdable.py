from abc import ABC
from typing import Any, Callable, override

from ..event        import EventManager
from ..inputmanager import InputManager, InputEvent
from .clickable     import Clickable

class Holdable(Clickable, ABC):
    """Abstract base class for UI elements that can be clicked and held.

    Extends Clickable to provide press-and-hold functionality with these features:
    - Press state tracking
    - Hold event handling
    - Release event handling
    - Continuous update while held
    - Priority-based event processing

    State Management:
    - Tracks pressed/released state
    - Handles hold duration
    - Manages release callbacks
    - Supports active/inactive states

    Event System:
    - Hold events during press
    - Release events on mouse up
    - Update events while held
    - Custom hold callbacks

    Attributes:
        _activeReleaseCallback (str): ID for release event handler
        _onHoldTriggerCallback (str): ID for hold state handler
        _onhold (str): Event ID for hold callbacks
        _isPressed (bool): Current press state
    """

    _activeReleaseCallback: str
    _onHoldTriggerCallback: str
    _onhold: str
    _isPressed: bool
    
    def __init__(self, buttonActive: bool=True) -> None:
        """Initialize a new holdable element.

        Sets up the hold and release event system and initializes state tracking.

        Args:
            buttonActive (bool, optional): Initial active state. Defaults to True.

        Raises:
            TypeError: If buttonActive is not a boolean
        """
        if not isinstance(buttonActive, bool):
            raise TypeError(f'buttonActive must be a boolean, got {type(buttonActive)}')
            
        Clickable.__init__(self, buttonActive)

        # Verify required methods exist
        if not hasattr(self, '_onRelease') or not callable(getattr(self, '_onRelease')):
            raise TypeError('Class must implement _onRelease method')
        if not hasattr(self, '_onHoldTrigger') or not callable(getattr(self, '_onHoldTrigger')):
            raise TypeError('Class must implement _onHoldTrigger method')

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
        """Handle button release event.

        Cleans up hold event subscription and updates press state.
        Called automatically when the button is released or deactivated.

        Side Effects:
            - Unsubscribes from update events
            - Sets pressed state to False
        """
        try:
            # Clean up hold trigger subscription
            updateEvent = InputManager.getEvent(InputEvent.UPDATE)
            if not updateEvent:
                raise ValueError('Failed to get UPDATE event ID')
            EventManager.unsubscribeToEvent(updateEvent, self._onHoldTriggerCallback)
        finally:
            # Ensure press state is cleared even if unsubscribe fails
            self._isPressed = False

    def _onHoldTrigger(self) -> None:
        """Handle continuous hold state updates.

        Triggers hold events while button is pressed and active.
        Automatically releases if button becomes inactive.

        Side Effects:
            - Triggers hold events if active
            - May trigger release if inactive
        """
        if self._buttonActive:
            try:
                EventManager.triggerEvent(self._onhold)
            except Exception as e:
                # If hold event fails, release to prevent stuck state
                self._onRelease()
                raise RuntimeError(f'Hold trigger failed: {str(e)}') from e
        else:
            self._onRelease()

    @override
    def _onTrigger(self) -> bool:
        """Handle initial button press.

        Sets up hold state tracking and event handling when button is first pressed.
        Maintains base click behavior from parent class.

        Returns:
            bool: True if trigger successful, False otherwise

        Side Effects:
            - Sets up hold event subscription
            - Updates press state
        """
        try:
            # First trigger base click behavior
            if not super()._onTrigger():
                return False

            # Set up hold tracking
            updateEvent = InputManager.getEvent(InputEvent.UPDATE)
            if not updateEvent:
                raise ValueError('Failed to get UPDATE event ID')
            
            if not EventManager.subscribeToEvent(updateEvent, self._onHoldTriggerCallback):
                raise RuntimeError('Failed to subscribe hold trigger')

            self._isPressed = True
            return True

        except Exception as e:
            # Clean up if setup fails
            self._isPressed = False
            raise RuntimeError(f'Trigger setup failed: {str(e)}') from e


    # -------------------- subscriptions --------------------

    def addReleaseEvent(self, event: str) -> bool:
        """Subscribe to an event that triggers button release.

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
        return EventManager.subscribeToEvent(event, self._activeReleaseCallback)
    
    def removeReleaseEvent(self, event: str) -> bool:
        """Remove a release event subscription.

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
        return EventManager.unsubscribeToEvent(event, self._activeReleaseCallback)

    def subscribeToHold(self, callback: str) -> bool:
        """Subscribe a callback to handle hold events.

        The callback will be triggered continuously while the button is held.

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
        return EventManager.subscribeToEvent(self._onhold, callback)
    
    def unsubscribeToHold(self, callback: str) -> bool:
        """Remove a hold event callback subscription.

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
        return EventManager.unsubscribeToEvent(self._onhold, callback)

    def quickSubscribeToHold(self, f: Callable, *args: Any) -> tuple[str, bool]:
        """Create and subscribe a new callback for hold events.

        Convenience method that wraps callback creation and subscription in one call.
        The callback will be triggered continuously while button is held.

        Args:
            f: Function to call during hold
            *args: Arguments to pass to the function

        Returns:
            tuple: (callback_id, subscription_success)
                callback_id: Identifier for the created callback
                subscription_success: True if subscription successful

        Raises:
            TypeError: If f is not callable

        Note:
            If subscription fails, the created callback will be cleaned up
            automatically to prevent resource leaks.
        """
        if not callable(f):
            raise TypeError(f'f must be callable, got {type(f)}')

        try:
            newCallback: str = EventManager.createCallback(f, *args)
            success = EventManager.subscribeToEvent(self._onhold, newCallback)

            if not success:
                # Clean up callback if subscription failed
                EventManager.removeCallback(newCallback)
                return ('', False)

            return (newCallback, True)

        except Exception as e:
            raise RuntimeError(f'Failed to create hold callback: {str(e)}') from e

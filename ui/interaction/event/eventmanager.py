from hashlib import sha256
from secrets import token_bytes
from typing  import Any, Callable

from .event     import Event
from .callback  import Callback


def getHashstring() -> str:
    return sha256(token_bytes(16)).hexdigest()


class EventManager:
    """
    Static manager class for the UI event system.

    Provides centralized management of events and callbacks with features:
    - Event creation and storage
    - Callback registration and management
    - Priority-based event handling
    - Event triggering and propagation control
    - Resource cleanup and management

    The event system supports:
    - Multiple subscribers per event
    - Priority-ordered execution
    - Event termination via boolean returns
    - Automatic resource cleanup
    - Thread-safe operation

    Usage:
        # Create an event
        event_id = EventManager.createEvent()

        # Create and subscribe a callback
        callback_id = EventManager.createCallback(my_function)
        EventManager.subscribeToEvent(event_id, callback_id)

        # Trigger the event
        EventManager.triggerEvent(event_id)

        # Clean up
        EventManager.removeCallback(callback_id)
    """
    
    __d_callbacks: dict[str, Callback] = {}   
    __d_events: dict[str, Event] = {}

    # -------------------- creation --------------------

    @staticmethod
    def createCallback(f: Callable, *args: Any, priority: int=0) -> str:
        """
        createCallback takes a function with its arguments and converts
        them into a callback which can be used to subscribe to events.
        Callbacks can return a bool. If they do, they act as event-terminators.

        Args:
            f    (Callable): function to used
            args (list[Any): arguments to be used

        Returns (str): the unique id of the callback
        """
        random_hashstring: str = getHashstring()
        while EventManager.__d_callbacks.get(random_hashstring):
            random_hashstring = getHashstring()

        event: Callback = Callback(f, *args, priority=priority) # create Callback
        EventManager.__d_callbacks[random_hashstring] = event # store Callback
        return random_hashstring

    @staticmethod
    def createEvent() -> str:
        """
        createEvent is used to create a new Event and store it in EventManager.
        It generates and returns the new Event name which is used to store and
        later trigger the event.

        Returns (str): the name of the new Event
        """
        random_hashstring: str = getHashstring()
        while EventManager.__d_events.get(random_hashstring):
            random_hashstring = getHashstring()

        event: Event = Event() # create Event
        EventManager.__d_events[random_hashstring] = event # store Event
        return random_hashstring

    # -------------------- getter --------------------

    @staticmethod
    def contains(name: str) -> bool:
        """
        contains returns if a Event with a given name is currently stored in
        Event Manager.

        Args:
            name (str): the event-name to look for

        Returns (bool): if the event is currently stored in EventManager
        """
        return bool(EventManager.__d_events.get(name, False))

    @staticmethod
    def getPriority(id: str) -> int:
        """
        getPriority returns the priority of the callback with the given id

        Args:
            id (str): id of the callback to access

        Returns (int): the priority of the callback (if it exists else -1)
        """
        if EventManager.__d_callbacks.get(id):
            return EventManager.__d_callbacks[id].getPriority()
        return -1

    # -------------------- setter --------------------

    @staticmethod
    def setPriority(id: str, priority: int) -> bool:
        """
        setPriority sets the priority of the callback with the given id
        to the given priority

        Args:
            id       (str): id of the callback to set the priority of
            priority (int): the new priority to set to the callback
        """
        if EventManager.__d_callbacks.get(id):
            EventManager.__d_callbacks[id].setPriority(priority)
            return True
        return False

    # -------------------- managing --------------------

    @staticmethod
    def __triggerCallback(name: str) -> bool:
        if EventManager.__d_callbacks.get(name):
            b = EventManager.__d_callbacks[name].call()
            if b: # if callback returns bool -> use as terminator
                return True
        return False

    @staticmethod
    def triggerEvent(name: str) -> bool:
        """
        triggerEvent triggers a Event with a given name if its currently stored
        in EventManager.

        Args:
            name (str): the event-name to trigger

        Returns (bool): if the event got triggered successfully
        """
        if EventManager.contains(name):
            callbacks: list[str] = EventManager.__d_events[name].trigger()
            if len(callbacks) > 1:
                callbacks.sort(key=lambda x: EventManager.getPriority(x), reverse=True)
            for clb in callbacks:
                if EventManager.__triggerCallback(clb):
                    break
            return True
        return False

    # -------------------- subscriptions --------------------

    @staticmethod
    def subscribeToEvent(event: str, callback: str) -> bool:
        """
        subscribeToEvent subscribes a given callback to a given Event is the
        Event is currently stored in EventManager.

        Args:
            event    (str): the event-name to subscribe the callback to
            callback (str): the callback to subscribe to the event

        Returns (bool): if the subscription got executed successfully
        """
        if EventManager.contains(event):
            EventManager.__d_events[event].subscribe(callback)
            return True
        return False
    
    @staticmethod
    def unsubscribeToEvent(event: str, callback: str) -> bool:
        """
        unsubscribe unsubscribes a callback (by id) from the event.

        Args:
            event    (str): the id of the event to unsubscribe to
            callback (str): the id of the callback to unsubscribe

        Returns (bool): if the unsubscription was successful
        """
        if EventManager.contains(event):
            return EventManager.__d_events[event].unsubscribe(callback)
        return False

    @staticmethod
    def quickSubscribe(event: str, f: Callable, *args: Any) -> tuple[str, bool]:
        """Create and subscribe a callback in one operation.

        Convenience method that creates a callback from a function and its
        arguments, then subscribes it to an event.

        Args:
            event: Event identifier to subscribe to
            f: Function to use as callback
            *args: Arguments to pass to the callback

        Returns:
            tuple: (callback_id, subscription_success)
                callback_id: Identifier for the created callback
                subscription_success: True if subscription successful

        Raises:
            TypeError: If event is not a string or f is not callable
            ValueError: If event is empty
        """
        if not isinstance(event, str):
            raise TypeError(f'event must be a string, got {type(event)}')
        if not event:
            raise ValueError('event identifier cannot be empty')
        if not callable(f):
            raise TypeError(f'f must be callable, got {type(f)}')

        try:
            newCallback: str = EventManager.createCallback(f, *args)
            success = EventManager.subscribeToEvent(event, newCallback)

            if not success:
                # Clean up callback if subscription failed
                EventManager.removeCallback(newCallback)
                return ('', False)

            return (newCallback, True)
        except Exception as e:
            # Ensure callback is cleaned up on any error
            if 'newCallback' in locals():
                EventManager.removeCallback(newCallback)
            raise RuntimeError(f'Failed to create and subscribe callback: {str(e)}') from e

    @staticmethod
    def removeCallback(callback_id: str) -> bool:
        """Remove a callback from the event system.

        Removes the callback with the given ID from the system and cleans up
        its resources. This should be called when a callback is no longer needed
        or if event subscription fails.

        Args:
            callback_id: Unique identifier of the callback to remove

        Returns:
            bool: True if callback was found and removed, False otherwise

        Raises:
            TypeError: If callback_id is not a string
            ValueError: If callback_id is empty
        """
        if not isinstance(callback_id, str):
            raise TypeError(f'callback_id must be a string, got {type(callback_id)}')
        if not callback_id:
            raise ValueError('callback_id cannot be empty')

        # Remove callback if it exists
        if callback_id in EventManager.__d_callbacks:
            del EventManager.__d_callbacks[callback_id]
            return True
            
        return False

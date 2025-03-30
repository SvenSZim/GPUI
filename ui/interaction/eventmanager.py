from hashlib import sha256
from secrets import token_bytes
from typing import Any, Callable

from .event import Event


class EventManager:
    """
    EventManager is a static class which is used to store and manage
    all UI related Events.
    """
    
    __d_events: dict[str, Event] = {}

    @staticmethod
    def createEvent() -> str:
        """
        createEvent is used to create a new Event and store it in EventManager.
        It generates and returns the new Event name which is used to store and
        later trigger the event.

        Returns:
            str = the name of the new Event
        """
        random_hashstring: str = sha256(token_bytes(16)).hexdigest()
        while EventManager.__d_events.get(random_hashstring):
            random_hashstring = sha256(token_bytes(16)).hexdigest()
        
        event: Event = Event(random_hashstring) # create Event
        EventManager.__d_events[random_hashstring] = event # store Event
        return random_hashstring

    @staticmethod
    def contains(name: str) -> bool:
        """
        contains returns if a Event with a given name is currently stored in
        Event Manager.

        Args:
            name: str = the event-name to look for

        Returns:
            bool = if the event is currently stored in EventManager
        """
        return bool(EventManager.__d_events.get(name, False))

    @staticmethod
    def triggerEvent(name: str) -> bool:
        """
        triggerEvent triggers a Event with a given name if its currently stored
        in EventManager.

        Args:
            name: str = the event-name to trigger

        Returns:
            bool = if the event got triggered successfully
        """
        if EventManager.contains(name):
            EventManager.__d_events[name].trigger()
            return True
        return False

    @staticmethod
    def subscribeToEvent(name: str, f: Callable, *args: Any) -> bool:
        """
        subscribeToEvent subscribes a given callback to a given Event is the
        Event is currently stored in EventManager.

        Args:
            name: str = the event-name to subscribe the callback to
            f: Callable = the function used to callback
            *args: Any = the arguments the function takes in

        Returns:
            bool = if the subscription got executed successfully
        """
        if EventManager.contains(name):
            EventManager.__d_events[name].subscribe(f, *args)
            return True
        return False

from hashlib import sha256
from secrets import token_bytes
from typing  import Any, Callable

from .event     import Event
from .callback  import Callback


def getHashstring() -> str:
    return sha256(token_bytes(16)).hexdigest()


class EventManager:
    """
    EventManager is a static class which is used to store and manage
    all UI related Events.
    """
    
    __d_callbacks: dict[str, Callback] = {}   
    __d_events: dict[str, Event] = {}

    # -------------------- creation --------------------

    @staticmethod
    def createCallback(f: Callable, *args: Any) -> str:
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

        event: Callback = Callback(f, *args) # create Callback
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
            for callback in EventManager.__d_events[name].trigger():
                if EventManager.__triggerCallback(callback):
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
        """
        quickSubscribe takes a function and its arguments, creates
        a Callback and subscribes to the event.

        Args:
            event (str)      : the event-name to subscribe to
            f     (Callable) : the function to use as callback
            args  (list[Any]): the arguments to use as callback

        Returns (tuple[str, bool]): 1. the id of the newly created Callback
                                    2. if the callback was successfully subscribed
        """
        newCallback: str = EventManager.createCallback(f, *args)
        return (newCallback, EventManager.subscribeToEvent(event, newCallback))



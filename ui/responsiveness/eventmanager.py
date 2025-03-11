from hashlib import sha256
from secrets import token_bytes
from typing import Any, Callable

from .event import Event


class EventManager:
    
    events: dict[str, Event] = {}

    @staticmethod
    def createEvent() -> str:
        random_hashstring: str = sha256(token_bytes(16)).hexdigest()
        while EventManager.events.get(random_hashstring):
            random_hashstring = sha256(token_bytes(16)).hexdigest()
        event: Event = Event(random_hashstring)
        EventManager.events[random_hashstring] = event
        return random_hashstring

    @staticmethod
    def contains(name: str) -> bool:
        if EventManager.events.get(name, False):
            return True
        return False

    @staticmethod
    def triggerEvent(name: str) -> bool:
        if EventManager.contains(name):
            EventManager.events[name].trigger()
            return True
        return False

    @staticmethod
    def subscribeToEvent(name: str, f: Callable, *args: Any) -> bool:
        if EventManager.contains(name):
            EventManager.events[name].subscribe(f, *args)
            return True
        return False

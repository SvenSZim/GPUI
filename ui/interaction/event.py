from typing import Any, Callable


class Event:
    """
    Event is a container class for Callables.
    It is used to create and store events which can be
    triggered or subscribed to.
    When triggered it calls all stored Callables (callbacks).
    """
    
    __name: str
    __l_subscriptions: list[tuple[Callable, list[Any]]]

    def __init__(self, name: str) -> None:
        """
        __init__ intializes the instance of Event

        Args:
            name: str = the name of the event
        """
        self.__name = name
        self.__l_subscriptions = []

    def subscribe(self, f: Callable, *args: Any) -> None:
        """
        subscribe takes a callback and adds it to the stored subscriptions

        Args:
            f: Callable = the function to add as callback
            *args: Any = the parameters the function takes in
        """
        self.__l_subscriptions.append((f, list(args)))

    def trigger(self) -> None:
        """
        trigger 'triggers' the event ~ all stored callbacks get called
        """
        _v_actual_subscriptions: list[tuple[Callable, list[Any]]] = self.__l_subscriptions.copy()
        for f, args in _v_actual_subscriptions:
            f(*args)

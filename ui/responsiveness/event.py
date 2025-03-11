

from typing import Any, Callable


class Event:
    
    name: str
    subscriptions: list[tuple[Callable, list[Any]]]

    def __init__(self, name: str) -> None:
        self.name = name
        self.subscriptions = []

    def subscribe(self, f: Callable, *args: Any) -> None:
        self.subscriptions.append((f, list(args)))

    def trigger(self) -> None:
        actual_subscriptions: list[tuple[Callable, list[Any]]] = self.subscriptions.copy()
        for f, args in actual_subscriptions:
            f(*args)

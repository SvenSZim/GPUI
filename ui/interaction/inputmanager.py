from abc import ABC, abstractmethod
from typing import Any, Callable, Optional

from .event import EventManager
from .inputevent import InputEvent

class InputHandler(ABC):
    inputEvents: dict[InputEvent, str] = {event: EventManager.createEvent() for event in list(InputEvent)}

    @staticmethod
    @abstractmethod
    def update() -> None:
        pass

    @staticmethod
    @abstractmethod
    def getMousePosition() -> tuple[int, int]:
        pass
    
    @staticmethod
    def getEvent(event: InputEvent) -> str:
        if InputHandler.inputEvents.get(event):
            return InputHandler.inputEvents[event]
        return ''

    @staticmethod
    def subscribeToEvent(event: InputEvent, callback: str) -> bool:
        if InputHandler.inputEvents.get(event):
            return EventManager.subscribeToEvent(InputHandler.inputEvents[event], callback)
        return False

    @staticmethod
    def quickSubscribe(event: InputEvent, f: Callable, *args: Any) -> bool:
        if InputHandler.inputEvents.get(event):
            return EventManager.quickSubscribe(InputHandler.inputEvents[event], f, *args)[1]
        return False

class InputManager:
    inputHandler: Optional[type[InputHandler]] = None

    @staticmethod
    def init(inputHandler: type[InputHandler]) -> None:
        InputManager.inputHandler = inputHandler


    @staticmethod
    def update() -> None:
        assert InputManager.inputHandler is not None
        InputManager.inputHandler.update()

    @staticmethod
    def getEvent(event: InputEvent) -> str:
        assert InputManager.inputHandler is not None
        return InputManager.inputHandler.getEvent(event)

    @staticmethod
    def subscribeToEvent(event: InputEvent, callback: str) -> bool:
        assert InputManager.inputHandler is not None
        return InputManager.inputHandler.subscribeToEvent(event, callback)

    @staticmethod
    def quickSubscribe(event: InputEvent, f: Callable, *args: Any) -> bool:
        assert InputManager.inputHandler is not None
        return InputManager.inputHandler.quickSubscribe(event, f, *args)

    @staticmethod
    def getMousePosition() -> tuple[int, int]:
        assert InputManager.inputHandler is not None
        return InputManager.inputHandler.getMousePosition()


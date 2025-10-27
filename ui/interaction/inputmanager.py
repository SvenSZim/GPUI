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
        """Initialize the input management system.
        
        Args:
            inputHandler: Implementation class for handling input events.
                         Must be a subclass of InputHandler.
                         
        Raises:
            TypeError: If inputHandler is not a subclass of InputHandler
        """
        if not issubclass(inputHandler, InputHandler):
            raise TypeError(
                f'Input handler must be a subclass of InputHandler, '
                f'got {inputHandler.__name__}'
            )
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
        """Subscribe a callback to an input event.
        
        Args:
            event: The input event to subscribe to
            callback: Name of the callback event to trigger
            
        Returns:
            bool: True if subscription was successful
            
        Raises:
            TypeError: If event is not an InputEvent
            ValueError: If callback is empty
        """
        if not isinstance(event, InputEvent):
            raise TypeError(f'event must be an InputEvent, got {type(event).__name__}')
        if not callback:
            raise ValueError('callback event name cannot be empty')
            
        assert InputManager.inputHandler is not None
        return InputManager.inputHandler.subscribeToEvent(event, callback)

    @staticmethod
    def quickSubscribe(event: InputEvent, f: Callable, *args: Any) -> bool:
        """Subscribe a function to be called when an input event occurs.
        
        Args:
            event: The input event to subscribe to
            f: Function to call when event occurs
            *args: Additional arguments to pass to the function
            
        Returns:
            bool: True if subscription was successful
            
        Raises:
            TypeError: If event is not an InputEvent or f is not callable
        """
        if not isinstance(event, InputEvent):
            raise TypeError(f'event must be an InputEvent, got {type(event).__name__}')
        if not callable(f):
            raise TypeError(f'f must be callable, got {type(f).__name__}')
            
        assert InputManager.inputHandler is not None
        return InputManager.inputHandler.quickSubscribe(event, f, *args)

    @staticmethod
    def getMousePosition() -> tuple[int, int]:
        assert InputManager.inputHandler is not None
        return InputManager.inputHandler.getMousePosition()


from typing import Any, Callable, Optional

class Callback:
    """
    A container for event callback functions with priority support.

    The Callback class encapsulates a function, its arguments, and a priority level
    for use in the event system. Callbacks can be executed with their stored
    arguments and can optionally return a boolean to control event propagation.

    Features:
    - Stores callable and its arguments
    - Supports priority levels for execution order
    - Optional boolean return for event termination
    - Thread-safe function execution

    Priority levels:
    - Higher numbers = higher priority
    - Default priority = 0
    - Negative priorities are allowed

    Example:
        def my_func(x: int) -> None: pass
        callback = Callback(my_func, 42, priority=1)
        result = callback.call()
    """
    __f: Callable     # function to call
    __args: list[Any] # arguments of the function to call
    __priority: int   # priority of the callback

    def __init__(self, f: Callable, *args: Any, priority: int=0) -> None:
        """
        Initialize a new Callback instance.

        Args:
            f: The function to be called
            *args: Arguments to pass to the function
            priority: Execution priority (higher = earlier), defaults to 0

        Raises:
            TypeError: If f is not callable or priority is not an integer
            ValueError: If priority is less than -1000 or greater than 1000
        """
        if not callable(f):
            raise TypeError(f'f must be callable, got {type(f)}')
        if not isinstance(priority, int):
            raise TypeError(f'priority must be an integer, got {type(priority)}')
        if not -1000 <= priority <= 1000:
            raise ValueError(f'priority must be between -1000 and 1000, got {priority}')
        self.__f = f
        self.__args = list(args)
        self.__priority = priority

    def call(self) -> Optional[bool]:
        """
        Execute the stored function with its arguments.

        Calls the callback function with its stored arguments in a thread-safe manner.
        If the function returns a boolean, it can be used to control event propagation.

        Returns:
            Optional[bool]: The function's return value if it returns a boolean,
                          otherwise None
        """
        result = self.__f(*self.__args)
        return result if isinstance(result, bool) else None

    def getPriority(self) -> int:
        """
        Get the callback's execution priority.

        Returns:
            int: The priority level of this callback
        """
        return self.__priority

    def setPriority(self, priority: int) -> None:
        """
        Set the callback's execution priority.

        Args:
            priority: New priority level (higher = earlier execution)

        Raises:
            TypeError: If priority is not an integer
            ValueError: If priority is outside valid range (-1000 to 1000)
        """
        if not isinstance(priority, int):
            raise TypeError(f'priority must be an integer, got {type(priority)}')
        if not -1000 <= priority <= 1000:
            raise ValueError(f'priority must be between -1000 and 1000, got {priority}')
        self.__priority = priority

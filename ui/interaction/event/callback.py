from typing import Any, Callable, Optional

class Callback:
    """
    Callback is a storage class for a callback of a event.
    """
    __f: Callable     # function to call
    __args: list[Any] # arguments of the function to call
    __priority: int   # priority of the callback

    def __init__(self, f: Callable, *args: Any, priority: int=0) -> None:
        self.__f = f
        self.__args = list(args)
        self.__priority = priority

    def call(self) -> Optional[bool]:
        """
        call calls the callback.
        """
        return self.__f(*self.__args)

    def getPriority(self) -> int:
        """
        returns the priority of the callback
        """
        return self.__priority

    def setPriority(self, priority: int) -> None:
        """
        setPriority sets the priority of the callback
        """
        self.__priority = priority

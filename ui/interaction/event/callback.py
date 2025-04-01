from typing import Any, Callable

class Callback:
    """
    Callback is a storage class for a callback of a event.
    """
    __f: Callable     # function to call
    __args: list[Any] # arguments of the function to call

    def __init__(self, f: Callable, *args: Any) -> None:
        self.__f = f
        self.__args = list(args)


    def call(self) -> None:
        """
        call calls the callback.
        """
        self.__f(*self.__args)

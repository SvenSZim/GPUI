from typing import Any, Callable, override

from ..UIABCComplex import UIABCComplex
from .UICTextCycleButtonCore import UICTextCycleButtonCore

class UICTextCycleButton(UIABCComplex[UICTextCycleButtonCore]):
    """
    UICTextCycleButton is a complex UIElement which consists of a button and a text where
    the text rotates through a list of strings by the press of the button.
    """

    def __init__(self, core: UICTextCycleButtonCore) -> None:
        
        super().__init__(core)

    @staticmethod
    @override
    def constructor(*args: Any, **kwargs: Any) -> 'UICTextCycleButton':
        return UICTextCycleButton(UICTextCycleButtonCore(*args, **kwargs))



    def subscribeToButtonEvent(self, state: str, f: Callable, *args: Any) -> bool:
        """
        subscribeToButtonEvent subscribes a Callback to the triggerEvent of the
        given buttonState of the UICycleButton.

        Args:
            state: str = the buttonState the Callback should be subscribed to
            f: Callable = the function that should be subscribed
            *args: Any = the potential arguments the function needs

        Returns:
            bool = returns if the subscription was successful
        """
        return self._core.subscribeToButtonEvent(state, f, *args)


    def subscribeToButtonClick(self, f: Callable, *args: Any) -> bool:
        """
        subscribeToButtonClick subscribes a Callback to the triggerEvent of
        all buttonStates of the UICycleButton.

        Args:
            f: Callable = the function that should be subscribed
            *args: Any = the potential arguments the function needs

        Returns:
            bool = returns if the subscriptions were successful
        """
        return self._core.subscribeToButtonClick(f, *args)




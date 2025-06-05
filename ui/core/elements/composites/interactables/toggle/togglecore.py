from typing import Any, override

from ......utility      import Rect
from ......interaction  import Togglable
from ..interactablecore import InteractableCore

class ToggleCore(InteractableCore, Togglable):
    """
    ToggleCore is the core object of the interactable 'Toggle'.
    """
    def __init__(self, numberOfStates: int, startState: int=0, buttonActive: bool=True) -> None:
        InteractableCore.__init__(self, Rect())
        Togglable.__init__(self, numberOfStates=numberOfStates, startState=startState, buttonActive=buttonActive)
    
    @override
    def getInnerSizing(self, elSize: tuple[int, int], args: dict[str, Any]) -> tuple[int, int]:
        return elSize

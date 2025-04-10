
from typing import Any, Callable
from ......utility      import Rect
from ......interaction  import Togglable
from ..interactablecore import InteractableCore

class TextCycleCore(InteractableCore, Togglable):
    """
    TextCycleCore is the core object of the interactable 'TextCycle'.
    """
    def __init__(self, rect: Rect, numberOfStates: int, startState: int=0, buttonActive: bool=True) -> None:
        InteractableCore.__init__(self, rect)
        Togglable.__init__(self, numberOfStates=numberOfStates, startState=startState, buttonActive=buttonActive)

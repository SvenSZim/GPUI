from typing import override

from ......utility      import Rect
from ......interaction  import Togglable
from ..interactablecore import InteractableCore

class CheckboxCore(InteractableCore, Togglable):
    """
    CheckboxCore is the core object of the interactable 'Checkbox'.
    """
    def __init__(self, rect: Rect, startState: bool=False, buttonActive: bool=True) -> None:
        InteractableCore.__init__(self, rect)
        Togglable.__init__(self, numberOfStates=2, startState=int(startState), buttonActive=buttonActive)

    @override
    def getInnerSizing(self, elSize: tuple[int, int]) -> tuple[int, int]:
        return elSize

from typing import override

from ......utility      import Rect
from ......interaction  import Holdable
from ..interactablecore import InteractableCore

class ButtonCore(InteractableCore, Holdable):
    """
    ButtonCore is the core object of the interactable 'Button'.
    """
    def __init__(self, rect: Rect, buttonActive: bool=True) -> None:
        InteractableCore.__init__(self, rect)
        Holdable.__init__(self, buttonActive=buttonActive)

    @override
    def getInnerSizing(self, elSize: tuple[int, int]) -> tuple[int, int]:
        return elSize

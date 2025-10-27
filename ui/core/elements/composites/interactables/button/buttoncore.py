from typing import Any, override

from ......utility      import Rect
from ......interaction  import Holdable
from ..interactablecore import InteractableCore

class ButtonCore(InteractableCore, Holdable):
    """Core implementation for Button elements managing press and hold states.
    
    Combines InteractableCore for basic interaction with Holdable for
    press-and-hold functionality. This class manages:
    - Button press state tracking
    - Hold duration monitoring
    - Press/release event handling
    - Click and hold callbacks
    
    The core maintains the button's interactive state and triggers
    appropriate callbacks based on user interaction patterns.
    """
    def __init__(self, buttonActive: bool=True) -> None:
        InteractableCore.__init__(self, Rect())
        Holdable.__init__(self, buttonActive=buttonActive)

    @override
    def getInnerSizing(self, elSize: tuple[int, int], args: dict[str, Any]) -> tuple[int, int]:
        return elSize

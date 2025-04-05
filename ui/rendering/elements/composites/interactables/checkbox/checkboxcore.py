
from ......utility      import Rect
from ......interaction  import Togglable
from ....element        import Element
from ..interactablecore import InteractableCore

class CheckboxCore(InteractableCore[Element], Togglable):
    """
    CheckboxCore is the core object of the interactable 'Checkbox'.
    """
    def __init__(self, rect: Rect, startState: bool=False, buttonActive: bool=True) -> None:
        InteractableCore.__init__(self, rect)
        Togglable.__init__(self, numberOfStates=2, startState=int(startState), buttonActive=buttonActive)

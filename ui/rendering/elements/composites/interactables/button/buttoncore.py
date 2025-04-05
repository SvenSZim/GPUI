
from ......utility      import Rect
from ......interaction  import Holdable
from ....element        import Element
from ..interactablecore import InteractableCore

class ButtonCore(InteractableCore[Element], Holdable):
    """
    ButtonCore is the core object of the interactable 'Button'.
    """
    def __init__(self, rect: Rect, buttonActive: bool=True) -> None:
        InteractableCore.__init__(self, rect)
        Holdable.__init__(self, buttonActive)

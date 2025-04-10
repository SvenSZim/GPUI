from abc import ABC

from .....utility       import Rect
from .....interaction   import Clickable
from ..compositioncore  import CompositionCore

class InteractableCore(CompositionCore, Clickable, ABC):

    def __init__(self, rect: Rect, buttonActive: bool=True) -> None:
        CompositionCore.__init__(self, rect)
        Clickable.__init__(self, buttonActive)

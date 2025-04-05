from abc import ABC

from .....utility   import Rect
from ..compositioncore  import CompositionCore

class InteractableCore(CompositionCore, ABC):

    def __init__(self, rect: Rect) -> None:
        super().__init__(rect)

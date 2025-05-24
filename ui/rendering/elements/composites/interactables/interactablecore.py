from abc import ABC

from .....utility       import Rect
from .....interaction   import Clickable
from ...elementcore  import ElementCore

class InteractableCore(ElementCore, Clickable, ABC):

    def __init__(self, rect: Rect) -> None:
        ElementCore.__init__(self, rect)

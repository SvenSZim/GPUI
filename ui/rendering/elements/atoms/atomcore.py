from abc import ABC

from ....utility import Rect
from ..core import ElementCore

class AtomCore(ElementCore, ABC):
    """
    AtomCore is the abstract base class for all ui-atom-element-cores.
    """

    # -------------------- creation --------------------

    def __init__(self, rect: Rect):
        super().__init__(rect)

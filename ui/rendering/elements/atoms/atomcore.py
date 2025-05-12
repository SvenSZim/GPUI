from abc import ABC, abstractmethod

from ....utility  import Rect
from ..elementcore import ElementCore

class AtomCore(ElementCore, ABC):
    """
    AtomCore is the abstract base class for all ui-atom-element-cores.
    """

    # -------------------- creation --------------------

    def __init__(self, rect: Rect):
        super().__init__(rect)

    @abstractmethod
    def copy(self) -> 'AtomCore':
        pass

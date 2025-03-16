from abc import ABC
from enum import Enum


class UIStylingElementOptions(Enum):
    """
    UIStylingData is the abstract base class for all UIStyleElements:

    Borders: 0x100 to 0x1FF
    Objects: 0x200 to 0x2FF
    Texts: 0x300 to 0x3FF
    """
    pass

class UIStyledElementData(ABC):
    pass

from dataclasses import dataclass
from typing import Optional

from ....generic import tColor
from ..styledborder import UISBorderData
from ..UIStylingABCData import UIStylingABCData

@dataclass
class UISButtonData(UIStylingABCData):
    borderData          : UISBorderData
    fillColor           : Optional[tColor]  = None
    stateDisplayStyle   : int               = 0
    stateDisplayColor   : Optional[tColor]  = None

from dataclasses import dataclass
from typing import Optional

from ....generic import tColor
from ..styledborder import UISBorderData
from ..UIStylingABCData import UIStylingABCData

@dataclass
class UISObjectData(UIStylingABCData):
    borderData  : UISBorderData
    fillColor   : Optional[tColor]  =   None
    doAlt       : bool              =   False
    altColor    : Optional[tColor]  =   None

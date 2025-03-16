from dataclasses import dataclass
from typing import Optional

from ....generic import tColor
from ..UIStylingABCData import UIStylingABCData

@dataclass
class UISBorderData(UIStylingABCData):
    doBorders   : tuple[bool, bool, bool, bool]     =   (False, False, False, False)
    mainColor   : Optional[tColor]                  =   None
    paritals    : tuple[float, float, float, float] =   (1.0, 1.0, 1.0, 1.0)
    doAlt       : bool                              =   False
    altColor    : Optional[tColor]                  =   None

from dataclasses import dataclass
from typing import Optional

from .....utility import Color
from ..atomdata import AtomData


bool4 = tuple[bool, bool, bool, bool]

@dataclass
class BoxData(AtomData):
    """
    BoxData is the storage class for all render-information
    for the atom 'Box'.
    """
    doBorders   : bool4             = (False, False, False, False) 
    fillColor   : Optional[Color]   = None
    doAlt       : bool              = False
    altColor    : Optional[Color]   = None

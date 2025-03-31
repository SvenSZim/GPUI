from dataclasses import dataclass
from typing import Optional

from .....utility import Color
from ..atomdata import AtomData


@dataclass
class LineData(AtomData):
    """
    LineData is the storage class for all render-information
    for the atom 'Line'.
    """

    mainColor   : Optional[Color]   = None
    partial     : float             = 1.0
    doAlt       : bool              = False
    altAbsLen   : Optional[float]   = None
    altColor    : Optional[Color]   = None
    flip        : bool              = False

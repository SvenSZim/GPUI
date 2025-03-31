from dataclasses import dataclass
from typing import Optional

from ....utility import Color
from ..atomdata import AtomData


@dataclass
class ToggleData(AtomData):
    """
    ToggleData is the storage class for all render-information
    for the atom 'Toggle'.
    """
    stateDispStyle  : int             = 0
    stateDispColor  : Optional[Color] = None


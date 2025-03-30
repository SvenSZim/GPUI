from dataclasses import dataclass
from typing import Optional

from ....utility import Color
from ..atomdata import AtomData


@dataclass
class ButtonData(AtomData):
    """
    ButtonData is the storage class for all render-information
    for the atom 'Button'.
    """
    stateDispStyle  : int             = 0
    stateDispColor  : Optional[Color] = None


from dataclasses import dataclass
from typing import Optional

from ....utility import Color
from ..atomdata import AtomData


@dataclass
class TextData(AtomData):
    """
    TextData is the storage class for all render-information
    for the atom 'Text'.
    """
    dynamicText : bool              = False
    textColor   : Optional[Color]   = None
    sysFontName : str               = 'Arial'
    fontSize    : Optional[int]     = 24


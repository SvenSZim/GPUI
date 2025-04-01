from dataclasses import dataclass
from typing import Optional

from ......utility import Color
from ..addondata import AddonData

none4 = (None, None, None, None)
bool4 = tuple[bool, bool, bool, bool]
float4 = tuple[float, float, float, float]
opfloat4 = tuple[Optional[float], Optional[float], Optional[float], Optional[float]]
color4 = tuple[Optional[Color], Optional[Color], Optional[Color], Optional[Color]]

@dataclass
class FramedData(AddonData):
    """
    FramedData is the storage class for all render-information
    for the addon 'Framed'.
    """
    borderColors    : color4            = none4
    borderParials   : float4            = (1.0, 1.0, 1.0, 1.0)
    borderDoAlts    : bool4             = (False, False, False, False)
    borderAltAbsLens: opfloat4          = none4
    borderAltColors : color4            = none4


    fillColor       : Optional[Color]   = None
    fillDoAlt       : bool              = False
    fillAltColor    : Optional[Color]   = None

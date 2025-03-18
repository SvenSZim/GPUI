from dataclasses import dataclass
from typing import Optional

from ...generic import Color
from ..UIABCRenderData import UIABCRenderData


@dataclass
class UILineRenderData(UIABCRenderData):
    mainColor   : Optional[Color]   = None
    partial     : float             = 1.0
    doAlt       : bool              = False
    altAbsLen   : Optional[float]   = None
    altColor    : Optional[Color]   = None

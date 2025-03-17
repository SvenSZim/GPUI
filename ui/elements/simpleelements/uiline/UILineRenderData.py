from dataclasses import dataclass
from typing import Optional

from ...generic import Color
from ..UIABCRenderData import UIABCRenderData


@dataclass
class UILineRenderData(UIABCRenderData):
    mainColor   : Optional[Color]   = None
    parital     : float             = 1.0
    doAlt       : bool              = False
    altColor    : Optional[Color]   = None

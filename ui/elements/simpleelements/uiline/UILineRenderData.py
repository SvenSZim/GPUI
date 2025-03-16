from dataclasses import dataclass
from typing import Optional

from ...generic import Color
from ..UIABCRenderData import UIABCRenderData

@dataclass
class UILineRenderData(UIABCRenderData):
    mainColor   : Optional[Color]                  =   None
    paritals    : tuple[float, float, float, float] =   (1.0, 1.0, 1.0, 1.0)
    doAlt       : bool                              =   False
    altColor    : Optional[Color]                  =   None

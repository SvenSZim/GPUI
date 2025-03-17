from dataclasses import dataclass
from typing import Optional

from ...generic import Color
from ..uiline import UISLine, UISLineCreateOptions
from ..UIABCRenderData import UIABCRenderData

bool4 = tuple[bool, bool, bool, bool]

@dataclass
class UIObjectRenderData(UIABCRenderData):
    borderData  : UISLine | list[UISLineCreateOptions]
    doBorders   : bool4             = (False, False, False, False) 
    fillColor   : Optional[Color]   = None
    doAlt       : bool              = False
    altColor    : Optional[Color]   = None

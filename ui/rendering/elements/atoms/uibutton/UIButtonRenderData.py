from dataclasses import dataclass
from typing import Optional

from ...generic import Color
from ..uiobject import UISObject, UISObjectCreateOptions
from ..UIABCRenderData import UIABCRenderData

@dataclass
class UIButtonRenderData(UIABCRenderData):
    objectData      : UISObject | list[UISObjectCreateOptions]
    stateDispStyle  : int               = 0
    stateDispColor  : Optional[Color]   = None


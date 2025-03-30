from dataclasses import dataclass
from typing import Optional

from ...generic import Color
from ..uiobject import UISObject, UISObjectCreateOptions
from ..UIABCRenderData import UIABCRenderData

@dataclass
class UITextRenderData(UIABCRenderData):
    objectData  : UISObject | list[UISObjectCreateOptions]
    dynamicText : bool              = False
    textColor   : Optional[Color]   = None
    sysFontName : str               = 'Arial'
    fontSize    : Optional[int]     = 24


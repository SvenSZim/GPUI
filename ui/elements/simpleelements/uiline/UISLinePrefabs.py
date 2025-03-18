from typing import Callable, override

from ...uirenderstyle import UIStyle, UIStyleManager
from ..uiline import UILineRenderData
from ..UIStyledABCPrefabs import UIStyledABCPrefabs
from .UILineRenderData import UILineRenderData
from .UISLine import UISLine

class UISLinePrefabs(UIStyledABCPrefabs[UISLine, UILineRenderData]):

    __prefabs: dict[UISLine, Callable[[UIStyle], UILineRenderData]] = {
        UISLine.INVISIBLE   : lambda _     : UILineRenderData(),
        UISLine.SOLID       : lambda style : UILineRenderData(UIStyleManager.getStyleColor(0, style)),
        UISLine.DOTTED      : lambda style : UILineRenderData(UIStyleManager.getStyleColor(0, style), doAlt=True, altAbsLen=10.0),
        UISLine.ALTERNATING : lambda style : UILineRenderData(UIStyleManager.getStyleColor(0, style), doAlt=True, altAbsLen=10.0, altColor=UIStyleManager.getStyleColor(1, style)),
        UISLine.SHRINKED    : lambda style : UILineRenderData(UIStyleManager.getStyleColor(0, style), partial=0.75),
        UISLine.SHRINKED_DOTTED:lambda style : UILineRenderData(UIStyleManager.getStyleColor(0, style), partial=0.75, doAlt=True, altAbsLen=10.0),
    }
    
    @override
    @staticmethod
    def getPrefabRenderData(uistyledid: UISLine, style: UIStyle) -> UILineRenderData:
        if UISLinePrefabs.__prefabs.get(uistyledid):
            return UISLinePrefabs.__prefabs[uistyledid](style)
        raise ValueError(f'UISLinePrefabs::uisobject={uistyledid} does not exist')


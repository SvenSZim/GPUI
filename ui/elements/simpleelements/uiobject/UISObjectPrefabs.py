from typing import Callable, override

from ...uirenderstyle import UIStyle, UIStyleManager
from ..uiline import UISLine
from ..UIStyledABCPrefabs import UIStyledABCPrefabs
from .UIObjectRenderData import UIObjectRenderData
from .UISObject import UISObject

class UISObjectPrefabs(UIStyledABCPrefabs[UISObject, UIObjectRenderData]):

    __prefabs: dict[UISObject, Callable[[UIStyle], UIObjectRenderData]] = {
        UISObject.INVISIBLE     : lambda style : UIObjectRenderData(borderData=UISLine.INVISIBLE),
        UISObject.BORDERONLY    : lambda style : UIObjectRenderData(borderData=UISLine.SOLID, doBorders=(True, True, True, True)),
        UISObject.SOLID         : lambda style : UIObjectRenderData(borderData=UISLine.SOLID, fillColor=UIStyleManager.getStyleColor(0, style)),
        UISObject.BORDER_TB     : lambda style : UIObjectRenderData(borderData=UISLine.SOLID, doBorders=(True, False, False, True)),
        UISObject.BASIC         : lambda style : UIObjectRenderData(borderData=UISLine.SOLID, doBorders=(True, True, True, True))
    }
    
    @override
    @staticmethod
    def getPrefabRenderData(uistyledid: UISObject, style: UIStyle) -> UIObjectRenderData:
        if UISObjectPrefabs.__prefabs.get(uistyledid):
            return UISObjectPrefabs.__prefabs[uistyledid](style)
        raise ValueError(f'UISObjectPrefabs::uisobject={uistyledid} does not exist')


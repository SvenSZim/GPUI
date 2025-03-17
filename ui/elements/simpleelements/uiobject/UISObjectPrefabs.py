from typing import override

from ..uiline import UILineRenderData
from ..UIStyledABCPrefabs import UIStyledABCPrefabs
from .UIObjectRenderData import UIObjectRenderData
from .UISObject import UISObject

class UISObjectPrefabs(UIStyledABCPrefabs[UISObject, UIObjectRenderData]):

    __prefabs: dict[UISObject, UIObjectRenderData] = {
        UISObject.INVISIBLE: UIObjectRenderData(borderData=UILineRenderData()),
        UISObject.BORDERONLY: UIObjectRenderData(borderData=UILineRenderData(mainColor='white'), doBorders=(True, True, True, True)),
        UISObject.SOLID: UIObjectRenderData(borderData=UILineRenderData(), fillColor='white'),
        UISObject.BORDER_TB: UIObjectRenderData(borderData=UILineRenderData(mainColor='white'), doBorders=(True, False, False, True)),
        UISObject.BASIC: UIObjectRenderData(borderData=UILineRenderData(mainColor='white'), doBorders=(True, True, True, True))
    }
    
    @override
    @staticmethod
    def getPrefabRenderData(uistyledid: UISObject) -> UIObjectRenderData:
        if UISObjectPrefabs.__prefabs.get(uistyledid):
            return UISObjectPrefabs.__prefabs[uistyledid]
        raise ValueError(f'UISObjectPrefabs::uisobject={uistyledid} does not exist')


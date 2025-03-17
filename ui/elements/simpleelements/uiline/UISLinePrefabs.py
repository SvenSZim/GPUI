from typing import override

from ..uiline import UILineRenderData
from ..UIStyledABCPrefabs import UIStyledABCPrefabs
from .UILineRenderData import UILineRenderData
from .UISLine import UISLine

class UISLinePrefabs(UIStyledABCPrefabs[UISLine, UILineRenderData]):

    __prefabs: dict[UISLine, UILineRenderData] = {
        UISLine.INVISIBLE: UILineRenderData(),
        UISLine.SOLID: UILineRenderData(mainColor='white'),
    }
    
    @override
    @staticmethod
    def getPrefabRenderData(uistyledid: UISLine) -> UILineRenderData:
        if UISLinePrefabs.__prefabs.get(uistyledid):
            return UISLinePrefabs.__prefabs[uistyledid]
        raise ValueError(f'UISLinePrefabs::uisobject={uistyledid} does not exist')


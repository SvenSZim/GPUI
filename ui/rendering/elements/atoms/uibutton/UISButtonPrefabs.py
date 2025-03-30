from typing import Callable, override

from ...uirenderstyle import UIStyle, UIStyleManager
from ..uiobject import UISObject
from ..UIStyledABCPrefabs import UIStyledABCPrefabs
from .UIButtonRenderData import UIButtonRenderData
from .UISButton import UISButton

class UISButtonPrefabs(UIStyledABCPrefabs[UISButton, UIButtonRenderData]):

    __prefabs: dict[UISButton, Callable[[UIStyle], UIButtonRenderData]] = {
        UISButton.INVISIBLE       : lambda _     : UIButtonRenderData(objectData=UISObject.INVISIBLE),
        UISButton.BASIC           : lambda _     : UIButtonRenderData(objectData=UISObject.BORDERONLY),
        UISButton.BASIC_FILLING   : lambda style : UIButtonRenderData(objectData=UISObject.BORDERONLY, stateDispStyle=1, stateDispColor=UIStyleManager.getStyleColor(0, style)),
        UISButton.BASIC_FILLING2  : lambda style : UIButtonRenderData(objectData=UISObject.BORDER_TB, stateDispStyle=1, stateDispColor=UIStyleManager.getStyleColor(1, style)),
    }
    
    @override
    @staticmethod
    def getPrefabRenderData(uistyledid: UISButton, style: UIStyle) -> UIButtonRenderData:
        if UISButtonPrefabs.__prefabs.get(uistyledid):
            return UISButtonPrefabs.__prefabs[uistyledid](style)
        raise ValueError(f'UISButtonPrefabs::uisobject={uistyledid} does not exist')


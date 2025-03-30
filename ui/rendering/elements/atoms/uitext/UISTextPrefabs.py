from typing import Callable, override

from ...uirenderstyle import UIStyle, UIStyleManager
from ..uiobject import UISObject
from ..UIStyledABCPrefabs import UIStyledABCPrefabs
from .UITextRenderData import UITextRenderData
from .UISText import UISText

class UISTextPrefabs(UIStyledABCPrefabs[UISText, UITextRenderData]):

    __prefabs: dict[UISText, Callable[[UIStyle], UITextRenderData]] = {
        UISText.INVISIBLE       : lambda _     : UITextRenderData(objectData=UISObject.BORDERONLY),
        UISText.NOBORDERS       : lambda style : UITextRenderData(objectData=UISObject.INVISIBLE, textColor=UIStyleManager.getStyleColor(0, style)),
        UISText.BASIC           : lambda style : UITextRenderData(objectData=UISObject.BORDERONLY, textColor=UIStyleManager.getStyleColor(0, style)),
        UISText.BASIC_TB        : lambda style : UITextRenderData(objectData=UISObject.BORDER_TB, textColor=UIStyleManager.getStyleColor(0, style)),
        UISText.DYNAMIC_BASIC   : lambda style : UITextRenderData(objectData=UISObject.BORDER_TB, dynamicText=True, textColor=UIStyleManager.getStyleColor(0, style)),
    }
    
    @override
    @staticmethod
    def getPrefabRenderData(uistyledid: UISText, style: UIStyle) -> UITextRenderData:
        if UISTextPrefabs.__prefabs.get(uistyledid):
            return UISTextPrefabs.__prefabs[uistyledid](style)
        raise ValueError(f'UISTextPrefabs::uisobject={uistyledid} does not exist')


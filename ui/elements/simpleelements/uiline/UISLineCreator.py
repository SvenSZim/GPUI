from typing import override

from ...uirenderstyle import UIStyle, UIStyleManager
from ..uiline import UILineRenderData
from ..UIStyledABCCreator import UIStyledABCCreator
from .UISLineCreateOptions import UISLineCreateOptions
from .UILineRenderData import UILineRenderData

class UISLineCreator(UIStyledABCCreator[UISLineCreateOptions, UILineRenderData]):

    @override
    @staticmethod
    def createStyledElement(createOptions: list[UISLineCreateOptions], style: UIStyle) -> UILineRenderData:
        lineData: UILineRenderData = UILineRenderData()

        for createOption in createOptions:
            match createOption:
                case UISLineCreateOptions.TRANSPARENT:
                    lineData.mainColor = None
                case UISLineCreateOptions.SOLID:
                    lineData.doAlt = False
                    if lineData.mainColor is None:
                        lineData.mainColor = UIStyleManager.getStyleColor(0, style)
                
                case UISLineCreateOptions.COLOR1:
                    lineData.mainColor = UIStyleManager.getStyleColor(0, style)
                case UISLineCreateOptions.COLOR2:
                    lineData.mainColor = UIStyleManager.getStyleColor(1, style)
        
        return lineData

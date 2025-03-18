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
            if 0x021 <= createOption.value <= 0x030:
                lineData.partial = 0.1 * (createOption.value - 0x020)
            match createOption:
                case UISLineCreateOptions.TRANSPARENT:
                    lineData.mainColor = None
                case UISLineCreateOptions.SOLID:
                    lineData.doAlt = False
                    if lineData.mainColor is None:
                        lineData.mainColor = UIStyleManager.getStyleColor(0, style)
                case UISLineCreateOptions.DOTTED:
                    lineData.doAlt = True
                    if lineData.mainColor is not None and lineData.altColor is not None:
                        lineData.altColor = None
                case UISLineCreateOptions.ALTERNATING:
                    lineData.doAlt = True
                    if lineData.mainColor is None:
                        lineData.mainColor = UIStyleManager.getStyleColor(0, style)
                    if lineData.altColor is None:
                        lineData.mainColor = UIStyleManager.getStyleColor(1, style)
                
                case UISLineCreateOptions.COLOR1:
                    lineData.mainColor = UIStyleManager.getStyleColor(0, style)
                case UISLineCreateOptions.COLOR2:
                    lineData.mainColor = UIStyleManager.getStyleColor(1, style)

                case UISLineCreateOptions.PARTIAL_NOPARTIAL:
                    lineData.partial = 1.0

                case UISLineCreateOptions.ALTLENGTH10:
                    lineData.altAbsLen = 10.0

                case UISLineCreateOptions.ALTCOLOR1:
                    lineData.altColor = UIStyleManager.getStyleColor(0, style)
                case UISLineCreateOptions.ALTCOLOR2:
                    lineData.altColor = UIStyleManager.getStyleColor(1, style)
        
        return lineData

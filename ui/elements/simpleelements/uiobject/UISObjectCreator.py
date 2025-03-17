from typing import override

from ...uirenderstyle import UIStyle, UIStyleManager
from ..uiline import UILineRenderData
from ..UIStyledABCCreator import UIStyledABCCreator
from .UISObjectCreateOptions import UISObjectCreateOptions
from .UIObjectRenderData import UIObjectRenderData

class UISObjectCreator(UIStyledABCCreator[UISObjectCreateOptions, UIObjectRenderData]):

    @override
    @staticmethod
    def createStyledElement(createOptions: list[UISObjectCreateOptions], style: UIStyle) -> UIObjectRenderData:
        borderData: UILineRenderData = UILineRenderData()
        objectData: UIObjectRenderData = UIObjectRenderData(borderData=borderData)

        for createOption in createOptions:
            match createOption:
                case UISObjectCreateOptions.BORDER_NOBORDER:
                    borderData = UILineRenderData()
                case UISObjectCreateOptions.BORDER_SOLID:
                    borderData.doAlt = False
                    if borderData.mainColor is None:
                        borderData.mainColor = UIStyleManager.getStyleColor(0, style)
                
                case UISObjectCreateOptions.BORDER_TOP:
                    objectData.doBorders = (True, objectData.doBorders[1], objectData.doBorders[2], objectData.doBorders[3])
                case UISObjectCreateOptions.BORDER_LEFT:
                    objectData.doBorders = (objectData.doBorders[0], True, objectData.doBorders[2], objectData.doBorders[3])
                case UISObjectCreateOptions.BORDER_RIGHT:
                    objectData.doBorders = (objectData.doBorders[0], objectData.doBorders[1], True, objectData.doBorders[3])
                case UISObjectCreateOptions.BORDER_BOTTOM:
                    objectData.doBorders = (objectData.doBorders[0], objectData.doBorders[1], objectData.doBorders[2], True)

                case UISObjectCreateOptions.BORDER_COLOR1:
                    borderData.mainColor = UIStyleManager.getStyleColor(0, style)
                case UISObjectCreateOptions.BORDER_COLOR2:
                    borderData.mainColor = UIStyleManager.getStyleColor(1, style)
 
                case UISObjectCreateOptions.FILL_NOFILL:
                    objectData.fillColor = None
                case UISObjectCreateOptions.FILL_SOLID:
                    objectData.doAlt = False
                    if objectData.fillColor is None:
                        objectData.fillColor = UIStyleManager.getStyleColor(0, style)
                
                case UISObjectCreateOptions.FILL_TOPLEFT:
                    pass
                case UISObjectCreateOptions.FILL_TOPRIGHT:
                    pass
                case UISObjectCreateOptions.FILL_BOTTOMLEFT:
                    pass
                case UISObjectCreateOptions.FILL_BOTTOMRIGHT:
                    pass

                case UISObjectCreateOptions.FILL_COLOR1:
                    objectData.fillColor = UIStyleManager.getStyleColor(0, style)
                case UISObjectCreateOptions.FILL_COLOR2:
                    objectData.fillColor = UIStyleManager.getStyleColor(1, style)
        
        objectData.borderData = borderData
        return objectData

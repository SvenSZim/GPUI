from typing import override

from ...uistyles import UIABCStyle
from ..styledborder import UISBorderData
from ..UIStyledABCCreator import UIStyledABCCreator
from .UISObjectCreateOptions import UISObjectCreateOptions
from .UISObjectData import UISObjectData
from .UISObjectRenderer import UISObjectRenderer

class UISObjectCreator(UIStyledABCCreator[UISObjectCreateOptions, UISObjectRenderer]):

    @override
    @staticmethod
    def createStyledObject(createOptions: list[UISObjectCreateOptions], style: UIABCStyle) -> UISObjectRenderer:
        borderData: UISBorderData = UISBorderData()
        objectData: UISObjectData = UISObjectData(borderData=borderData)

        for createOption in createOptions:
            match createOption:
                case UISObjectCreateOptions.BORDER_NOBORDER:
                    borderData = UISBorderData()
                case UISObjectCreateOptions.BORDER_SOLID:
                    borderData.doAlt = False
                    if borderData.mainColor is None:
                        borderData.mainColor = style.getStyleColor(0)
                
                case UISObjectCreateOptions.BORDER_TOP:
                    borderData.doBorders = (True, borderData.doBorders[1], borderData.doBorders[2], borderData.doBorders[3])
                case UISObjectCreateOptions.BORDER_LEFT:
                    borderData.doBorders = (borderData.doBorders[0], True, borderData.doBorders[2], borderData.doBorders[3])
                case UISObjectCreateOptions.BORDER_RIGHT:
                    borderData.doBorders = (borderData.doBorders[0], borderData.doBorders[1], True, borderData.doBorders[3])
                case UISObjectCreateOptions.BORDER_BOTTOM:
                    borderData.doBorders = (borderData.doBorders[0], borderData.doBorders[1], borderData.doBorders[2], True)

                case UISObjectCreateOptions.BORDER_COLOR1:
                    borderData.mainColor = style.getStyleColor(0)
                case UISObjectCreateOptions.BORDER_COLOR2:
                    borderData.mainColor = style.getStyleColor(1)

                case UISObjectCreateOptions.FILL_NOFILL:
                    objectData.fillColor = None
                case UISObjectCreateOptions.FILL_SOLID:
                    objectData.doAlt = False
                    if objectData.fillColor is None:
                        objectData.fillColor = style.getStyleColor(0)
                
                case UISObjectCreateOptions.FILL_TOPLEFT:
                    pass
                case UISObjectCreateOptions.FILL_TOPRIGHT:
                    pass
                case UISObjectCreateOptions.FILL_BOTTOMLEFT:
                    pass
                case UISObjectCreateOptions.FILL_BOTTOMRIGHT:
                    pass

                case UISObjectCreateOptions.FILL_COLOR1:
                    objectData.fillColor = style.getStyleColor(0)
                case UISObjectCreateOptions.FILL_COLOR2:
                    objectData.fillColor = style.getStyleColor(1)
        
        objectData.borderData = borderData
        return UISObjectRenderer(objectData)

from typing import override

from ...uirenderstyle import UIStyle, UIStyleManager
from ..uiobject import UISObjectCreateOptions
from ..UIStyledABCCreator import UIStyledABCCreator
from .UISButtonCreateOptions import UISButtonCreateOptions
from .UIButtonRenderData import UIButtonRenderData

class UISButtonCreator(UIStyledABCCreator[UISButtonCreateOptions, UIButtonRenderData]):

    @override
    @staticmethod
    def createStyledElement(createOptions: list[UISButtonCreateOptions], style: UIStyle) -> UIButtonRenderData:
        objectData: list[UISObjectCreateOptions] = []
        buttonData: UIButtonRenderData = UIButtonRenderData(objectData=objectData)

        for createOption in createOptions:
            if createOption.value < 0x200:
                objectData.append(UISObjectCreateOptions(createOption.value))
                continue
            match createOption:
                case UISButtonCreateOptions.BUTTON_NOSTATE:
                    buttonData.stateDispColor = None
                case UISButtonCreateOptions.BUTTON_STATE1:
                    buttonData.stateDispStyle = 1
                    if buttonData.stateDispColor is None:
                        buttonData.stateDispColor = UIStyleManager.getStyleColor(0, style)
                case UISButtonCreateOptions.BUTTON_STATE2:
                    buttonData.stateDispStyle = 2
                    if buttonData.stateDispColor is None:
                        buttonData.stateDispColor = UIStyleManager.getStyleColor(0, style)
                case UISButtonCreateOptions.BUTTON_STATE3:
                    buttonData.stateDispStyle = 3
                    if buttonData.stateDispColor is None:
                        buttonData.stateDispColor = UIStyleManager.getStyleColor(0, style)

                case UISButtonCreateOptions.BUTTON_COLOR1:
                    buttonData.stateDispColor = UIStyleManager.getStyleColor(0, style)
                case UISButtonCreateOptions.BUTTON_COLOR2:
                    buttonData.stateDispColor = UIStyleManager.getStyleColor(1, style)
        
        buttonData.objectData = objectData
        return buttonData

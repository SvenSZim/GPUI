from typing import override

from ...uirenderstyle import UIStyle, UIStyleManager
from ..uiobject import UISObjectCreateOptions
from ..UIStyledABCCreator import UIStyledABCCreator
from .UISTextCreateOptions import UISTextCreateOptions
from .UITextRenderData import UITextRenderData

class UISTextCreator(UIStyledABCCreator[UISTextCreateOptions, UITextRenderData]):

    @override
    @staticmethod
    def createStyledElement(createOptions: list[UISTextCreateOptions], style: UIStyle) -> UITextRenderData:
        objectData: list[UISObjectCreateOptions] = []
        textData: UITextRenderData = UITextRenderData(objectData=objectData)

        for createOption in createOptions:
            if createOption.value < 0x200:
                objectData.append(UISObjectCreateOptions(createOption.value))
                continue
            match createOption:
                case UISTextCreateOptions.TEXT_NOTEXT:
                    textData.textColor = None
                case UISTextCreateOptions.TEXT_SOLID:
                    if textData.textColor is None:
                        textData.textColor = UIStyleManager.getStyleColor(0, style)

                case UISTextCreateOptions.TEXT_STATIC:
                    textData.dynamicText = False
                    if textData.fontSize is None:
                        textData.fontSize = 24
                case UISTextCreateOptions.TEXT_DYNAMIC:
                    textData.dynamicText = True
                    textData.fontSize = None

                case UISTextCreateOptions.TEXT_COLOR1:
                    textData.textColor = UIStyleManager.getStyleColor(0, style)
                case UISTextCreateOptions.TEXT_COLOR2:
                    textData.textColor = UIStyleManager.getStyleColor(1, style)
        
        textData.objectData = objectData
        return textData

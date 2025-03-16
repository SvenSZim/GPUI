from typing import override

from .UIABCStyle import UIABCStyle

from ..uistyledprefabs import UISBorderData
from ..uistyledprefabs import UISObject, UISObjectData, UISObjectRenderer
from ..uistyledprefabs import UISText, UISTextData, UISTextRenderer
from ..uistyledprefabs import UISButton, UISButtonData, UISButtonRenderer


class UIStyleFIRE(UIABCStyle):
    """
    MOON is a storage class for the UIStyleObjects of the MOON-Style
    """

    @override
    @staticmethod
    def getStyledObject(styledobject: UISObject) -> UISObjectRenderer:
        styledObjectData: UISObjectData
        match styledobject:
            case _:
                borderData: UISBorderData = UISBorderData(doBorders=(True, True, True, True), borderColor='red')
                styledObjectData = UISObjectData(borderData=borderData, doFill=False, fillColor='red')

        return UISObjectRenderer(styledObjectData)

    
    @override
    @staticmethod
    def getStyledText(styledtext: UISText) -> UISTextRenderer:
        styledTextData: UISTextData
        match styledtext:
            case _:
                borderData: UISBorderData = UISBorderData(doBorders=(True, True, True, True), borderColor='red')
                styledTextData = UISTextData(borderData=borderData, doFill=False, fillColor='red')

        return UISTextRenderer(styledTextData)

    
    @override
    @staticmethod
    def getStyledButton(styledbutton: UISButton) -> UISButtonRenderer:
        styledButtonData: UISButtonData
        match styledbutton:
            case _:
                borderData: UISBorderData = UISBorderData(doBorders=(True, True, True, True), borderColor='red')
                styledButtonData = UISButtonData(borderData=borderData, doFill=False, fillColor='red')

        return UISButtonRenderer(styledButtonData)


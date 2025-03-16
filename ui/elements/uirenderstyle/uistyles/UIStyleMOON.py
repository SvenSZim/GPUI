from typing import override

from ...generic import tColor

from .UIABCStyle import UIABCStyle

from ..uistyledprefabs import UISBorderData
from ..uistyledprefabs import UISObject, UISObjectData, UISObjectRenderer
from ..uistyledprefabs import UISText, UISTextData, UISTextRenderer
from ..uistyledprefabs import UISButton, UISButtonData, UISButtonRenderer

color1: tColor = 'white'
color2: tColor = 'blue'

class UIStyleMOON(UIABCStyle):
    """
    MOON is a storage class for the UIStyleObjects of the MOON-Style
    """

    @override
    @staticmethod
    def getStyledObject(styledobject: UISObject) -> UISObjectRenderer:
        styledObjectData: UISObjectData
        match styledobject:
            case UISObject.BORDERONLY:
                borderData: UISBorderData = UISBorderData(doBorders=(True, True, True, True), mainColor=color1)
                styledObjectData = UISObjectData(borderData=borderData)
            case UISObject.SOLID:
                borderData: UISBorderData = UISBorderData(doBorders=(True, True, True, True), mainColor=color1)
                styledObjectData = UISObjectData(borderData=borderData, fillColor=color2)
            case UISObject.BORDER_TB:
                borderData: UISBorderData = UISBorderData(doBorders=(True, False, False, True), mainColor=color1)
                styledObjectData = UISObjectData(borderData=borderData)
            case _:
                borderData: UISBorderData = UISBorderData(doBorders=(True, True, True, True), borderColor='white')
                styledObjectData = UISObjectData(borderData=borderData, doFill=False, fillColor='white')
        
        return UISObjectRenderer(styledObjectData)

    
    @override
    @staticmethod
    def getStyledText(styledtext: UISText) -> UISTextRenderer:
        styledTextData: UISTextData
        match styledtext:
            case UISText.NOBORDERS:
                styledTextData = UISTextData(borderData=UISBorderData())
            case UISText.SOLID:
                borderData: UISBorderData = UISBorderData(doBorders=(True, True, True, True), mainColor=color1)
                styledTextData = UISTextData(borderData=borderData, fillColor=color2)
            case _:
                borderData: UISBorderData = UISBorderData(doBorders=(True, True, True, True), borderColor='white')
                styledTextData = UISTextData(borderData=borderData, doFill=False, fillColor='white')
        
        return UISTextRenderer(styledTextData)

    
    @override
    @staticmethod
    def getStyledButton(styledbutton: UISButton) -> UISButtonRenderer:
        styledButtonData: UISButtonData
        match styledbutton:
            case UISButton.NOBORDERS:
                styledButtonData = UISButtonData(borderData=UISBorderData(), fillColor=color2, stateDisplayColor=color1)
            case UISButton.SOLID:
                borderData: UISBorderData = UISBorderData(doBorders=(True, True, True, True), mainColor=color1)
                styledButtonData = UISButtonData(borderData=borderData, fillColor=color2, stateDisplayColor=color1)
            case _:
                borderData: UISBorderData = UISBorderData(doBorders=(True, True, True, True), borderColor='white')
                styledButtonData = UISButtonData(borderData=borderData, doFill=False, fillColor='white')

        return UISButtonRenderer(styledButtonData)

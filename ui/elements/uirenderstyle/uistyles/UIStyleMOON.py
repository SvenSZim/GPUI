from typing import override

from ...generic import tColor

from ..uistyledprefabs import UISBorderData
from ..uistyledprefabs import UISObject, UISObjectData, UISObjectRenderer, UISObjectCreateOptions, UISObjectCreator
from ..uistyledprefabs import UISText, UISTextData, UISTextRenderer
from ..uistyledprefabs import UISButton, UISButtonData, UISButtonRenderer
from ..UIStyle import UIStyle

from .UIABCStyle import UIABCStyle

colors: list[tColor] = ['white', (205, 205, 205), (150, 150, 150)]

class UIStyleMOON(UIABCStyle):
    """
    MOON is a storage class for the UIStyleObjects of the MOON-Style
    """
    @override
    @staticmethod
    def getStyleColor(colorIndex: int) -> tColor:
        return colors[colorIndex]

    @override
    @staticmethod
    def getStyledObject(styledobject: UISObject) -> UISObjectRenderer:
        styledObjectData: UISObjectData
        match styledobject:
            case UISObject.INVISIBLE:
                styledObjectData = UISObjectData(borderData=UISBorderData())
            case UISObject.BORDERONLY:
                borderData: UISBorderData = UISBorderData(doBorders=(True, True, True, True), mainColor=colors[0])
                styledObjectData = UISObjectData(borderData=borderData)
            case UISObject.SOLID:
                borderData: UISBorderData = UISBorderData()
                styledObjectData = UISObjectData(borderData=borderData, fillColor=colors[0])
            case UISObject.BORDER_TB:
                borderData: UISBorderData = UISBorderData(doBorders=(True, False, False, True), mainColor=colors[0])
                styledObjectData = UISObjectData(borderData=borderData)
            case UISObject.BASIC:
                borderData: UISBorderData = UISBorderData(doBorders=(True, True, True, True), mainColor=colors[0])
                styledObjectData = UISObjectData(borderData=borderData)
            case _:
                borderData: UISBorderData = UISBorderData(doBorders=(True, True, True, True), mainColor=colors[0])
                styledObjectData = UISObjectData(borderData=borderData, fillColor=colors[0])
        
        return UISObjectRenderer(styledObjectData)

    @override
    @staticmethod
    def createStyledObject(styledObjectCreationData: list[UISObjectCreateOptions]) -> UISObjectRenderer:
        return UISObjectCreator.createStyledObject(styledObjectCreationData, UIStyleMOON)
        

    
    @override
    @staticmethod
    def getStyledText(styledtext: UISText) -> UISTextRenderer:
        styledTextData: UISTextData
        match styledtext:
            case UISText.INVISIBLE:
                styledTextData = UISTextData(borderData=UISBorderData())
            case UISText.NOBORDERS:
                styledTextData = UISTextData(borderData=UISBorderData())
            case UISText.SOLID:
                borderData: UISBorderData = UISBorderData(doBorders=(True, True, True, True), mainColor=colors[0])
                styledTextData = UISTextData(borderData=borderData, fillColor=colors[0])
            case UISText.BASIC:
                borderData: UISBorderData = UISBorderData(doBorders=(True, True, True, True), mainColor=colors[0])
                styledTextData = UISTextData(borderData=borderData)
            case _:
                borderData: UISBorderData = UISBorderData(doBorders=(True, True, True, True), mainColor=colors[0])
                styledTextData = UISTextData(borderData=borderData, fillColor=colors[0])
        
        return UISTextRenderer(styledTextData)

    
    @override
    @staticmethod
    def getStyledButton(styledbutton: UISButton) -> UISButtonRenderer:
        styledButtonData: UISButtonData
        match styledbutton:
            case UISButton.INVISIBLE:
                styledButtonData = UISButtonData(borderData=UISBorderData())
            case UISButton.NOBORDERS:
                styledButtonData = UISButtonData(borderData=UISBorderData(), stateDisplayColor=colors[0])
            case UISButton.SOLID:
                borderData: UISBorderData = UISBorderData(doBorders=(True, True, True, True), mainColor=colors[0])
                styledButtonData = UISButtonData(borderData=borderData, fillColor=colors[0], stateDisplayColor='black')
            case UISButton.BASIC:
                borderData: UISBorderData = UISBorderData(doBorders=(True, True, True, True), mainColor=colors[0])
                styledButtonData = UISButtonData(borderData=borderData, stateDisplayColor=colors[0])
            case _:
                borderData: UISBorderData = UISBorderData(doBorders=(True, True, True, True), borderColor='white')
                styledButtonData = UISButtonData(borderData=borderData, doFill=False, fillColor='white')

        return UISButtonRenderer(styledButtonData)



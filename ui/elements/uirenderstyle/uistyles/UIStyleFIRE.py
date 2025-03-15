from typing import override

from .UIABCStyle import UIABCStyle

from ...generic import Color
from ..uistyledelements import UIStyledObjects, UIStyledTexts, UIStyledButtons
from ..uistyledelements import UIABCStyledObject, UIABCStyledText, UIABCStyledButton

from ..uistyledelements import UIStyledObjectBasic, UIStyledTextBasic, UIStyledButtonBasic


class UIStyleFIRE(UIABCStyle):
    """
    MOON is a storage class for the UIStyleObjects of the MOON-Style
    """

    @override
    @staticmethod
    def getStyledObject(styledobject: UIStyledObjects) -> UIABCStyledObject:
        match styledobject:
            case UIStyledObjects.BASIC:
                return UIStyledObjectBasic(borderColor='red')
            case _:
                return UIStyledObjectBasic(borderColor='red')



    @override
    @staticmethod
    def getStyledText(styledtext: UIStyledTexts) -> UIABCStyledText:
        match styledtext:
            case UIStyledTexts.BASIC:
                return UIStyledTextBasic(borderColor='red')
            case _:
                return UIStyledTextBasic(borderColor='red')


    @override
    @staticmethod
    def getStyledButton(styledbutton: UIStyledButtons) -> UIABCStyledButton:
        match styledbutton:
            case UIStyledButtons.BASIC:
                return UIStyledButtonBasic(borderColor='red', buttonStateFillColor=Color((255, 102, 0)))
            case _:
                return UIStyledButtonBasic(borderColor='red', buttonStateFillColor=Color((255, 102, 0)))

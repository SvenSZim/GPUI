from typing import override

from .UIABCStyle import UIABCStyle

from ..uistyledelements import UIStyledObjects, UIStyledTexts, UIStyledButtons
from ..uistyledelements import UIABCStyledObject, UIABCStyledText, UIABCStyledButton

from ..uistyledelements import UIStyledObjectBasic, UIStyledTextBasic, UIStyledButtonBasic


class UIStyleMOON(UIABCStyle):
    """
    MOON is a storage class for the UIStyleObjects of the MOON-Style
    """

    @override
    @staticmethod
    def getStyledObject(styledobject: UIStyledObjects) -> UIABCStyledObject:
        match styledobject:
            case UIStyledObjects.BASIC:
                return UIStyledObjectBasic(borderColor='white')


    @override
    @staticmethod
    def getStyledText(styledtext: UIStyledTexts) -> UIABCStyledText:
        match styledtext:
            case UIStyledTexts.BASIC:
                return UIStyledTextBasic(borderColor='white')


    @override
    @staticmethod
    def getStyledButton(styledbutton: UIStyledButtons) -> UIABCStyledButton:
        match styledbutton:
            case UIStyledButtons.BASIC:
                return UIStyledButtonBasic(borderColor='white', buttonStateFillColor='white')

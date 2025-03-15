from typing import override

from .UIABCStyle import UIABCStyle

from ..uistyledelements import UIStyledObjects, UIStyledTexts, UIStyledButtons
from ..uistyledelements import UIABCStyledObject, UIABCStyledText, UIABCStyledButton

from ..uistyledelements import UIStyledObjectBasic, UIStyledObjectPartial
from ..uistyledelements import UIStyledTextBasic
from ..uistyledelements import UIStyledButtonBasic


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
            case UIStyledObjects.BASIC_90:
                return UIStyledObjectPartial(UIStyledObjectBasic, 0.9, borderColor='white')
            case UIStyledObjects.BASIC_75:
                return UIStyledObjectPartial(UIStyledObjectBasic, 0.75, borderColor='white')
            case UIStyledObjects.BASIC_50:
                return UIStyledObjectPartial(UIStyledObjectBasic, 0.50, borderColor='white')
            case UIStyledObjects.BASIC_25:
                return UIStyledObjectPartial(UIStyledObjectBasic, 0.25, borderColor='white')
            case UIStyledObjects.BASIC_10:
                return UIStyledObjectPartial(UIStyledObjectBasic, 0.10, borderColor='white')
            case _:
                return UIStyledObjectBasic(borderColor='white')


    @override
    @staticmethod
    def getStyledText(styledtext: UIStyledTexts) -> UIABCStyledText:
        match styledtext:
            case UIStyledTexts.BASIC:
                return UIStyledTextBasic(borderColor='white')
            case UIStyledTexts.BASIC_NOBORDER:
                return UIStyledTextBasic()
            case _:
                return UIStyledTextBasic(borderColor='white')


    @override
    @staticmethod
    def getStyledButton(styledbutton: UIStyledButtons) -> UIABCStyledButton:
        match styledbutton:
            case UIStyledButtons.BASIC:
                return UIStyledButtonBasic(borderColor='white', buttonStateFillColor='white')
            case _:
                return UIStyledButtonBasic(borderColor='white', buttonStateFillColor='white')

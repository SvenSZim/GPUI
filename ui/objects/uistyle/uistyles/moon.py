from typing import override

from .UIABCStyle import UIABCStyle

from ..uistyleelements import UIStyleObjects, UIStyleTexts, UIStyleButtons
from ..uistyleelements import UIABCStyleObject, UIABCStyleText, UIABCStyleButton

from ..uistyleelements import UIStyleObjectBasic, UIStyleTextBasic, UIStyleButtonBasic


class UIStyleMOON(UIABCStyle):
    """
    MOON is a storage class for the UIStyleObjects of the MOON-Style
    """

    @override
    @staticmethod
    def getStyledObject(styleobject: UIStyleObjects) -> UIABCStyleObject:
        match styleobject:
            case UIStyleObjects.BASIC:
                return UIStyleObjectBasic(borderColor='white')


    @override
    @staticmethod
    def getStyledText(styletext: UIStyleTexts) -> UIABCStyleText:
        match styletext:
            case UIStyleTexts.BASIC:
                return UIStyleTextBasic(borderColor='white')


    @override
    @staticmethod
    def getStyledButton(stylebutton: UIStyleButtons) -> UIABCStyleButton:
        match stylebutton:
            case UIStyleButtons.BASIC:
                return UIStyleButtonBasic(borderColor='white', buttonStateFillColor='white')

from abc import ABC, abstractmethod

from ..uistyleelements import UIStyleObjects, UIABCStyleObject
from ..uistyleelements import UIStyleTexts, UIABCStyleText
from ..uistyleelements import UIStyleButtons, UIABCStyleButton


class UIABCStyle(ABC):
    """
    UIABCStyle is the abstract base class for all UIStyles.
    """

    @staticmethod
    @abstractmethod
    def getStyledObject(styleobject: UIStyleObjects) -> UIABCStyleObject:
        pass

    @staticmethod
    @abstractmethod
    def getStyledText(styletext: UIStyleTexts) -> UIABCStyleText:
        pass

    @staticmethod
    @abstractmethod
    def getStyledButton(stylebutton: UIStyleButtons) -> UIABCStyleButton:
        pass

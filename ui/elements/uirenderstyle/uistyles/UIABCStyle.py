from abc import ABC, abstractmethod

from ..uistyledelements import UIStyledObjects, UIABCStyledObject
from ..uistyledelements import UIStyledTexts, UIABCStyledText
from ..uistyledelements import UIStyledButtons, UIABCStyledButton


class UIABCStyle(ABC):
    """
    UIABCStyle is the abstract base class for all UIStyles.
    """

    @staticmethod
    @abstractmethod
    def getStyledObject(styledobject: UIStyledObjects) -> UIABCStyledObject:
        pass

    @staticmethod
    @abstractmethod
    def getStyledText(styledtext: UIStyledTexts) -> UIABCStyledText:
        pass

    @staticmethod
    @abstractmethod
    def getStyledButton(styledbutton: UIStyledButtons) -> UIABCStyledButton:
        pass

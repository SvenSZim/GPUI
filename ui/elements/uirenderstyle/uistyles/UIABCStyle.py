from abc import ABC, abstractmethod

from ..uistyledprefabs import UISObject, UISObjectRenderer
from ..uistyledprefabs import UISText, UISTextRenderer
from ..uistyledprefabs import UISButton, UISButtonRenderer


class UIABCStyle(ABC):
    """
    UIABCStyle is the abstract base class for all UIStyles.
    """

    @staticmethod
    @abstractmethod
    def getStyledObject(styledobject: UISObject) -> UISObjectRenderer:
        pass

    @staticmethod
    @abstractmethod
    def getStyledText(styledtext: UISText) -> UISTextRenderer:
        pass

    @staticmethod
    @abstractmethod
    def getStyledButton(styledbutton: UISButton) -> UISButtonRenderer:
        pass

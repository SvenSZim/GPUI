from abc import ABC, abstractmethod

from ...generic import tColor
from ..uistyledprefabs import UISObject, UISObjectRenderer, UISObjectCreateOptions
from ..uistyledprefabs import UISText, UISTextRenderer
from ..uistyledprefabs import UISButton, UISButtonRenderer


class UIABCStyle(ABC):
    """
    UIABCStyle is the abstract base class for all UIStyles.
    """

    @staticmethod
    @abstractmethod
    def getStyleColor(colorIndex: int) -> tColor:
        pass

    @staticmethod
    @abstractmethod
    def getStyledObject(styledobject: UISObject) -> UISObjectRenderer:
        pass

    @staticmethod
    @abstractmethod
    def createStyledObject(styledObjectCreationData: list[UISObjectCreateOptions]) -> UISObjectRenderer:
        pass

    @staticmethod
    @abstractmethod
    def getStyledText(styledtext: UISText) -> UISTextRenderer:
        pass

    """
    @staticmethod
    @abstractmethod
    def createStyledText(styledTextData: UISTextData) -> UISTextRenderer:
        pass
    """

    @staticmethod
    @abstractmethod
    def getStyledButton(styledbutton: UISButton) -> UISButtonRenderer:
        pass
    
    """
    @staticmethod
    @abstractmethod
    def createStyledButton(styledButtonData: UISButtonData) -> UISButtonRenderer:
        pass
    """

from abc import ABC, abstractmethod

from ...generic import Color


class UIABCStyle(ABC):
    """
    UIABCStyle is the abstract base class for all UIStyles.
    """

    @staticmethod
    @abstractmethod
    def getStyleColor(colorIndex: int) -> Color:
        pass

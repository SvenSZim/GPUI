from abc import ABC, abstractmethod

from ....utility import Color


class ABCStyle(ABC):
    """
    UIABCStyle is the abstract base class for all UIStyles.
    """

    @staticmethod
    @abstractmethod
    def getStyleColor(colorIndex: int) -> Color:
        """
        getStyleColor is a method which returns the style-specific color of the given index

        Args:
            colorIndex (int): the index of the color

        Returns (Color): the requested Color
        """
        pass

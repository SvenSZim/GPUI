from abc import ABC, abstractmethod

from ..generic import tColor
from .UISurface import UISurface

class UIFont(ABC):
    """
    UIFont is the abstract base class of all fonts used in the UI.
    It defines some needed functionality which needs to be implemented as interface.
    """

    @abstractmethod
    def render(self, text: str, color: tColor) -> UISurface:
        """
        render creates a UISurface with the given text rendered on top.

        Args:
            text: str = the text that is to be drawn
            color: Color = the color which should be used to draw the text
        
        Returns:
            UISurface = the surface with the text rendered on top
        """
        pass

    @staticmethod
    @abstractmethod
    def SysFont(name: str, fontsize: int) -> 'UIFont':
        """
        SysFont (staticmethod) creates a UIFont instance of the systemfont with
        the given name and the given fontsize.

        Args: 
            name: str = the name of the systemfont
            fontsize: int = the fontsize describes the fontsize

        Returns:
            UIFont = a instance of UIFont with the given specs
        """
        pass


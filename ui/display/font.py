from abc import ABC, abstractmethod

from ..utility import Color
from .surface import Surface

class Font(ABC):
    """
    Font is the abstract base class of all fonts used in the UI.
    It defines some needed functionality which needs to be implemented as interface.
    """

    @abstractmethod
    def render(self, text: str, color: Color) -> Surface:
        """
        render creates a Surface with the given text rendered on top.

        Args:
            text    (str)  : the text that is to be drawn
            color   (Color): the color which should be used to draw the text
        
        Returns (Surface): the surface with the text rendered on top
        """
        pass

    @staticmethod
    @abstractmethod
    def SysFont(name: str, fontsize: int) -> 'Font':
        """
        SysFont (staticmethod) creates a Font instance of the systemfont with
        the given name and the given fontsize.

        Args: 
            name        (str): the name of the systemfont
            fontsize    (int): the fontsize describes the fontsize

        Returns (Font): a instance of Font with the given specs
        """
        pass


from abc import ABC
from typing import override

from ..uidrawerinterface import UISurface
from ..UIRenderer import UIRenderer

class UIABCComplex(UIRenderer, ABC):
    """
    UIABCComplex is the abstract base class for all complex ui elements
    """
    
    _simpleelements: list[UIRenderer]

    def __init__(self, simpleelements: list[UIRenderer]) -> None:
        """
        __init__ initializes the values of UIABCComplex for the complex ui element.

        Args:
            simpleelements: list[UIABCRenderer] = list of simple UIElements the element consists of
        """
        self._simpleelements = simpleelements

    @override
    def render(self, surface: UISurface) -> None:
        """
        render renders the UIElement with the given style onto the given surface.

        Args:
            surface: UISurface = the surface the UIElement should be drawn on
        """
        for simpleelement in self._simpleelements:
            simpleelement.render(surface)

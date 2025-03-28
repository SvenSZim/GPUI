from abc import ABC
from typing import Generic, TypeVar, override

from ..uidrawerinterface import UISurface
from ..UIRenderer import UIRenderer
from .UIABCComplexCore import UIABCComplexCore

Core = TypeVar('Core', bound=UIABCComplexCore)

class UIABCComplex(Generic[Core], UIRenderer[Core], ABC):
    """
    UIABCComplex is the abstract base class for all complex ui elements
    """
    
    def __init__(self, core: Core) -> None:
        """
        __init__ initializes the values of UIABCComplex for the complex ui element.

        Args:
            simpleelements: list[UIABCRenderer] = list of simple UIElements the element consists of
        """
        super().__init__(core)

    @override
    def render(self, surface: UISurface) -> None:
        """
        render renders the UIElement with the given style onto the given surface.

        Args:
            surface: UISurface = the surface the UIElement should be drawn on
        """
        for simpleelement in self._core.getSimpleElements():
            simpleelement.render(surface)

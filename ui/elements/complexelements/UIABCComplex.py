from abc import ABC
from typing import override

from ..uidrawerinterface import UISurfaceDrawer, UISurface
from ..uirenderstyle import UIABCStyle
from ..simpleelements import UIABCRenderer
from ..UIRenderer import UIRenderer

class UIABCComplex(UIRenderer, ABC):
    """
    UIABCComplex is the abstract base class for all complex ui elements
    """
    
    _simpleelements: list[UIABCRenderer]

    def __init__(self, simpleelements: list[UIABCRenderer]) -> None:
        """
        __init__ initializes the values of UIABCComplex for the complex ui element.

        Args:
            simpleelements: list[UIABCRenderer] = list of simple UIElements the element consists of
        """
        self._simpleelements = simpleelements

    @override
    def render(self, surfaceDrawer: type[UISurfaceDrawer], surface: UISurface) -> None:
        pass

    @override
    def renderStyled(self, surfaceDrawer: type[UISurfaceDrawer], surface: UISurface, renderStyle: type[UIABCStyle]) -> None:
        """
        renderStyled renders the UIElement with the given style onto the given surface.

        Args:
            surfaceDrawer: UISurfaceDrawer = the drawer to use when drawing on the surface
            surface: UISurface = the surface the UIElement should be drawn on
            renderStyle: UIStyle = the renderstyle used to render
        """
        for simpleelement in self._simpleelements:
            simpleelement.renderStyled(surfaceDrawer, surface, renderStyle)

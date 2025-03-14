from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from .idrawer import UISurfaceDrawer, UISurface
from .UIABC import UIABC

Core = TypeVar('Core', bound=UIABC)

class UIABCRenderer(Generic[Core], ABC):
    """
    UIABCRenderer is the abstract base class for all UIElementRenderers.
    UIElementRenderers consist of the corresponding UIElement and some renderInfo.
    """
    
    _active: bool # boolean if the renderer is active or not
    _core: Core # refering UIElement which gets rendered by the Renderer

    def __init__(self, core: Core, active: bool=True) -> None:
        """
        __init__ initializes the values of UIABCRenderer for the UIElementRenderer

        Args:
            core: Core (bound=UIABC) = the refering UIElement of the UIElementRenderer
            active: bool = the start active-state of the UIElementRenderer
        """
        self._active = active
        self._core = core

    def isActive(self) -> bool:
        """
        isActive returns the active-state of the Renderer

        Returns:
            bool = active-state of the Renderer
        """
        return self._active

    def toggleActive(self) -> bool:
        """
        toggleActive toggles the active-state of the Renderer

        Returns:
            bool = new active-state of the Renderer
        """
        self._active = not self._active
        return self._active

    def setActive(self, active: bool) -> None:
        """
        setActive sets the active-state of the Renderer

        Args:
            active: bool = new active-state of the Renderer
        """
        self._active = active

    def update(self) -> None:
        """
        update updates the positioning and sizing of the refering UIElement
        """
        self._core.update()

    
    @abstractmethod
    def render(self, surfaceDrawer: UISurfaceDrawer, surface: UISurface) -> None:
        """
        render renders the UIElement onto the given surface

        Args:
            surfaceDrawer: UISurfaceDrawer = the drawer to use when drawing on the surface
            surface: UISurface = the surface the UIElement should be drawn on
        """
        pass

    """
    @abstractmethod
    def renderStyled(self, surfaceDrawer: UISurfaceDrawer, surface: UISurface, renderStyle: UIStyle) -> None:
        pass
    """


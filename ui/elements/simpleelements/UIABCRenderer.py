from abc import ABC
from typing import Generic, Optional, TypeVar

from ..uirenderstyle import UIStyledElements
from ..UIRenderer import UIRenderer
from .UIABC import UIABC

Core = TypeVar('Core', bound=UIABC)
StyleElem = TypeVar('StyleElem', bound=UIStyledElements)

class UIABCRenderer(Generic[Core, StyleElem], UIRenderer, ABC):
    """
    UIABCRenderer is the abstract base class for all UIElementRenderers.
    UIElementRenderers consist of the corresponding UIElement and some renderInfo.
    """
    
    _active: bool # boolean if the renderer is active or not
    _core: Core # refering UIElement which gets rendered by the Renderer
    _renderStyleElement: Optional[StyleElem] # used style-element for rendering

    def __init__(self, core: Core, active: bool, renderStyleElement: Optional[StyleElem]) -> None:
        """
        __init__ initializes the values of UIABCRenderer for the UIElementRenderer

        Args:
            core: Core (bound=UIABC) = the refering UIElement of the UIElementRenderer
            active: bool = the start active-state of the UIElementRenderer
            renderStyleElement: StyleElem = the render style that should be used when rendering styled
        """
        self._active = active
        self._core = core
        self._renderStyleElement = renderStyleElement

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


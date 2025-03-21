from abc import ABC
from typing import Generic, TypeVar

from ..UIRenderer import UIRenderer
from .UIABCCore import UIABCCore
from .UIABCRenderData import UIABCRenderData

Core = TypeVar('Core', bound=UIABCCore)
RenderData = TypeVar('RenderData', bound=UIABCRenderData)

class UIABC(Generic[Core, RenderData], UIRenderer[Core], ABC):
    """
    UIABCRenderer is the abstract base class for all UIElementRenderers.
    UIElementRenderers consist of the corresponding UIElement and some renderInfo.
    """
    
    _active: bool # boolean if the renderer is active or not
    _renderData: RenderData # used style-element for rendering

    def __init__(self, core: Core, active: bool, renderData: RenderData) -> None:
        """
        __init__ initializes the values of UIABCRenderer for the UIElementRenderer

        Args:
            core: Core (bound=UIABC) = the refering UIElement of the UIElementRenderer
            active: bool = the start active-state of the UIElementRenderer
            renderStyleElement: StyleElem = the render style that should be used when rendering styled
        """
        super().__init__(core)
        self._active = active
        self._renderData = renderData


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


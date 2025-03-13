from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar

from .generic import Rect
from .idrawer import UISurface
from .UIABC import UIABC

B = TypeVar('B', bound=UIABC)

class UIABCRenderer(Generic[B], ABC):
    """
    UIABCRenderer is the abstract base class for all UIElementRenderers.
    UIElementRenderers consist of the corresponding UIElement and some renderInfo.
    """
    
    active: bool
    body: B

    def getActive(self) -> bool:
        """
        getActive returns the active-state of the Renderer

        Returns:
            bool = active-state of the Renderer
        """
        return self.active

    def toggleActive(self) -> bool:
        """
        toggleActive toggles the active-state of the Renderer

        Returns:
            bool = new active-state of the Renderer
        """
        self.active = not self.active
        return self.active

    def setActive(self, active: bool) -> None:
        """
        setActive sets the active-state of the Renderer

        Args:
            active: bool = new active-state of the Renderer
        """
        self.active = active


    def getUIObject(self) -> B:
        """
        getUIObject returns the corresponding UIObject from the UIElementRenderer

        Returns:
            B (bound=UIABC): Corresponding UIObject
        """
        return self.body

    def update(self) -> None:
        """
        update updates the positioning and sizing of the UIElement
        """
        self.getUIObject().update()

    
    @abstractmethod
    def render(self, surface: UISurface) -> None:
        """
        render renders the UIElement onto the given surface

        Args:
            surface: UISurface = the surface the UIElement should be drawn on
        """
        pass


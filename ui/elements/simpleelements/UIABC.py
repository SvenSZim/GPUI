from abc import ABC
from typing import Generic, TypeVar, override

from ..generic import Rect
from ..UIRenderer import UIRenderer
from .uibody import UIABCBody
from .UIABCCore import UIABCCore
from .UIABCRenderData import UIABCRenderData

Core = TypeVar('Core', bound=UIABCCore)
RenderData = TypeVar('RenderData', bound=UIABCRenderData)

class UIABC(Generic[Core, RenderData], UIRenderer[Core], UIABCBody, ABC):
    """
    UIABCRenderer is the abstract base class for all UIElementRenderers.
    UIElementRenderers consist of the corresponding UIElement and some renderInfo.
    """
    
    _renderData: RenderData # used style-element for rendering

    def __init__(self, core: Core, active: bool, renderData: RenderData) -> None:
        """
        __init__ initializes the values of UIABCRenderer for the UIElementRenderer

        Args:
            core: Core (bound=UIABC) = the refering UIElement of the UIElementRenderer
            active: bool = the start active-state of the UIElementRenderer
            renderStyleElement: StyleElem = the render style that should be used when rendering styled
        """
        UIRenderer.__init__(self, core, active)
        UIABCBody.__init__(self, self._core.getBody().getRect())
        
        self._renderData = renderData

    @override
    def update(self) -> None:
        self._core.update()
        self._rect = self._core.getBody().getRect()

    #DEBUG
    def setWidth(self, newW: int) -> None:
        self._rect = Rect(self.getPosition(), (newW, self._rect.height))
        self._core._body._rect = self._rect

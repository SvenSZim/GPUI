from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from ...uidrawerinterface import UISurfaceDrawer, UISurface
from .UIStyledElementData import UIStyledElementData


StylingData = TypeVar('StylingData', bound=UIStyledElementData)
RenderData = TypeVar('RenderData')

class UIStyledABCRenderer(Generic[StylingData, RenderData], ABC):
    """
    UIABCStyleElement is the abstract base class for all UIStyleElements
    """
    
    _stylingData: UIStyledElementData
    def __init__(self, stylingData: UIStyledElementData) -> None:
        self._stylingData = stylingData


    @abstractmethod
    def render(self, surfaceDrawer: type[UISurfaceDrawer], surface: UISurface, renderData: RenderData) -> None:
        pass

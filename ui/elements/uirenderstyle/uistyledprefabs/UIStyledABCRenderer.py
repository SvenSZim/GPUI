from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from ...uidrawerinterface import UISurfaceDrawer, UISurface
from .UIStylingABCData import UIStylingABCData

StylingData = TypeVar('StylingData', bound=UIStylingABCData)
RenderData = TypeVar('RenderData')

class UIStyledABCRenderer(Generic[StylingData, RenderData], ABC):

    _stylingData: StylingData

    def __init__(self, stylingData: StylingData) -> None:
        self._stylingData = stylingData

    @abstractmethod
    def render(self, surfaceDrawer: type[UISurfaceDrawer], surface: UISurface, renderData: RenderData) -> None:
        pass


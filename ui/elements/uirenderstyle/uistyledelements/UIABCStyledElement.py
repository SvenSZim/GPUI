from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from ...uidrawerinterface import UISurfaceDrawer, UISurface


RenderData = TypeVar('RenderData')

class UIABCStyledElement(Generic[RenderData], ABC):
    """
    UIABCStyleElement is the abstract base class for all UIStyleElements
    """
    @abstractmethod
    def render(self, surfaceDrawer: type[UISurfaceDrawer], surface: UISurface, data: RenderData) -> None:
        pass

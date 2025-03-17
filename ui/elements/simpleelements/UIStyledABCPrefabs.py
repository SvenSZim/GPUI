from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from .UIStyledABC import UIStyledABC
from .UIABCRenderData import UIABCRenderData


StyledElement = TypeVar('StyledElement', bound=UIStyledABC)
RenderData = TypeVar('RenderData', bound=UIABCRenderData)

class UIStyledABCPrefabs(Generic[StyledElement, RenderData], ABC):

    @staticmethod
    @abstractmethod
    def getPrefabRenderData(uistyledid: StyledElement) -> RenderData:
        pass

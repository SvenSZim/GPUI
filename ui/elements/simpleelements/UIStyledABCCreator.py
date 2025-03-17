from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from ..uirenderstyle import UIStyle
from .UIStylingABCCreateOptions import UIStylingABCCreateOptions
from .UIABCRenderData import UIABCRenderData

CreateOptions = TypeVar('CreateOptions', bound=UIStylingABCCreateOptions)
RenderData = TypeVar('RenderData', bound=UIABCRenderData)

class UIStyledABCCreator(Generic[CreateOptions, RenderData], ABC):

    @staticmethod
    @abstractmethod
    def createStyledElement(createOptions: list[CreateOptions], style: UIStyle) -> RenderData:
        pass

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from ..uistyles import UIABCStyle
from .UIStylingABCCreateOptions import UIStylingABCCreateOptions
from .UIStyledABCRenderer import UIStyledABCRenderer

CreateOptions = TypeVar('CreateOptions', bound=UIStylingABCCreateOptions)
Renderer = TypeVar('Renderer', bound=UIStyledABCRenderer)

class UIStyledABCCreator(Generic[CreateOptions, Renderer], ABC):

    @staticmethod
    @abstractmethod
    def createStyledObject(createOptions: list[CreateOptions], style: UIABCStyle) -> Renderer:
        pass

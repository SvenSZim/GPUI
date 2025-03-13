
from abc import ABC, abstractmethod
from typing import Union

from ..generic import Color
from .UISurface import UISurface

class UIFont(ABC):

    @abstractmethod
    def render(self, text: str, color: Union[str, tuple[int, int, int], Color]) -> UISurface:
        pass

    @staticmethod
    @abstractmethod
    def SysFont(name: str, fontsize: int) -> 'UIFont':
        pass


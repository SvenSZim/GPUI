from abc import ABC, abstractmethod
from typing import Union

from ..generic import Color, Rect
from .UISurface import UISurface

class UISurfaceDrawer(ABC):

    @abstractmethod
    def drawline(self, surface: UISurface, startpoint: tuple[int, int], endpoint: tuple[int, int], color: Union[str, tuple[int, int, int], Color]) -> None:
        pass

    @abstractmethod
    def drawrect(self, surface: UISurface, rect: Rect, color: Union[str, tuple[int, int, int], Color], fill: bool = True) -> None:
        pass

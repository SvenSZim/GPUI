import pygame as pg

from typing import Union, override
from ui import UISurface, UIFont, UISurfaceDrawer, Color, Rect


class PygameSurface(UISurface):
    surface: pg.Surface
    def __init__(self, surface: pg.Surface) -> None:
        self.surface = surface

    @override
    def getSize(self) -> tuple[int, int]:
        return self.surface.get_size()

    @override
    def blit(self, surface: 'UISurface', position: tuple[int, int]) -> None:
        """
        Combines the two surfaces
        """
        if isinstance(surface, PygameSurface):
            self.surface.blit(surface.surface, position)

class PygameFont(UIFont):
    font: pg.font.Font

    def __init__(self, font: pg.font.Font) -> None:
        self.font = font

    @override
    def render(self, text: str, color: Union[str, tuple[int, int, int], Color]) -> UISurface:
        if isinstance(color, Color):
            color = color.value
        return PygameSurface(self.font.render(text, True, pg.Color(color)))

    @override
    @staticmethod
    def SysFont(name: str, fontsize: int) -> 'UIFont':
        return PygameFont(pg.font.SysFont(name, fontsize))

class PygameDrawer(UISurfaceDrawer):
    @override
    @staticmethod
    def drawline(surface: UISurface, startpoint: tuple[int, int], endpoint: tuple[int, int], color: Union[str, tuple[int, int, int], Color]) -> None:
        if isinstance(color, Color):
            color = color.value
        if isinstance(surface, PygameSurface):
            pg.draw.line(surface.surface, color, startpoint, endpoint)


    @override
    @staticmethod
    def drawrect(surface: UISurface, rect: Rect, color: Union[str, tuple[int, int, int], Color], fill: bool = True) -> None:
        if isinstance(color, Color):
            color = color.value
        if isinstance(surface, PygameSurface):
            pg.draw.rect(surface.surface, color, pg.Rect((rect.left, rect.top), (rect.width, rect.height)))



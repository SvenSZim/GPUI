import pygame as pg

from typing import override
from ui import Surface, Font, SurfaceDrawer, Color, tColor, Rect


class PygameSurface(Surface):
    surface: pg.Surface
    def __init__(self, surface: pg.Surface) -> None:
        self.surface = surface

    @override
    def getSize(self) -> tuple[int, int]:
        return self.surface.get_size()

    @override
    def blit(self, surface: 'Surface', position: tuple[int, int]) -> None:
        """
        Combines the two surfaces
        """
        if isinstance(surface, PygameSurface):
            self.surface.blit(surface.surface, position)

class PygameFont(Font):
    font: pg.font.Font

    def __init__(self, font: pg.font.Font) -> None:
        self.font = font

    @override
    def render(self, text: str, color: Color) -> Surface:
        if isinstance(color, tColor):
            color = color.value
        return PygameSurface(self.font.render(text, True, pg.Color(color)))

    @override
    @staticmethod
    def SysFont(name: str, fontsize: int) -> 'Font':
        return PygameFont(pg.font.SysFont(name, fontsize))

class PygameDrawer(SurfaceDrawer):
    @override
    @staticmethod
    def drawline(surface: Surface, startpoint: tuple[int, int], endpoint: tuple[int, int], color: Color, thickness: int=1) -> None:
        if isinstance(color, tColor):
            color = color.value
        if isinstance(surface, PygameSurface):
            pg.draw.line(surface.surface, color, startpoint, endpoint, width=thickness)


    @override
    @staticmethod
    def drawrect(surface: Surface, rect: Rect, color: Color, fill: bool = True) -> None:
        if isinstance(color, tColor):
            color = color.value
        if isinstance(surface, PygameSurface):
            if fill:
                pg.draw.rect(surface.surface, color, pg.Rect((rect.left, rect.top), (rect.width, rect.height)))
            else:
                pg.draw.line(surface.surface, color, (rect.left, rect.top), (rect.right, rect.top))
                pg.draw.line(surface.surface, color, (rect.left, rect.top), (rect.left, rect.bottom))
                pg.draw.line(surface.surface, color, (rect.right, rect.top), (rect.right, rect.bottom))
                pg.draw.line(surface.surface, color, (rect.left, rect.bottom), (rect.right, rect.bottom))

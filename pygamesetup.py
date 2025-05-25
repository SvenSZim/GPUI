import pygame as pg

from typing import override
from ui import Surface, Font, SurfaceDrawer, EventManager, InputEvent, InputHandler, Color, tColor, Rect


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

class PygameInputHandler(InputHandler):
    currentDown: set[InputEvent] = set()

    @staticmethod
    @override
    def update() -> None:
        for event in pg.event.get():
            match event.type:
                case pg.QUIT:
                    EventManager.triggerEvent(PygameInputHandler.inputEvents[InputEvent.QUIT])
                case pg.KEYDOWN:
                    if pg.key.get_pressed()[pg.K_ESCAPE]:
                        EventManager.triggerEvent(PygameInputHandler.inputEvents[InputEvent.QUIT])
                    if pg.key.get_pressed()[pg.K_LEFT]:
                        EventManager.triggerEvent(PygameInputHandler.inputEvents[InputEvent.ARR_LEFT])
                    if pg.key.get_pressed()[pg.K_RIGHT]:
                        EventManager.triggerEvent(PygameInputHandler.inputEvents[InputEvent.ARR_RIGHT])
                    for c in range(ord('a'), ord('z')+1):
                        if pg.key.get_pressed()[pg.key.key_code(chr(c))]:
                            EventManager.triggerEvent(PygameInputHandler.inputEvents[InputEvent.fromStr(chr(c))])
                            PygameInputHandler.currentDown.add(InputEvent.fromStr(chr(c)))
                case pg.KEYUP:
                    for c in range(ord('a'), ord('z')+1):
                        if InputEvent.fromStr(chr(c)) in PygameInputHandler.currentDown and not pg.key.get_pressed()[pg.key.key_code(chr(c))]:
                            EventManager.triggerEvent(PygameInputHandler.inputEvents[InputEvent((InputEvent.fromStr(chr(c))).value + 1)])
                            PygameInputHandler.currentDown.remove(InputEvent.fromStr(chr(c)))
                case pg.MOUSEBUTTONDOWN:
                    EventManager.triggerEvent(PygameInputHandler.inputEvents[InputEvent.MOUSEBUTTONDOWN])
                    if InputEvent.LEFTHELD not in PygameInputHandler.currentDown and pg.mouse.get_pressed()[0]:
                        EventManager.triggerEvent(PygameInputHandler.inputEvents[InputEvent.LEFTDOWN])
                        PygameInputHandler.currentDown.add(InputEvent.LEFTHELD)
                case pg.MOUSEBUTTONUP:
                    EventManager.triggerEvent(PygameInputHandler.inputEvents[InputEvent.MOUSEBUTTONUP])
                    if InputEvent.LEFTHELD in PygameInputHandler.currentDown and not pg.mouse.get_pressed()[0]:
                        EventManager.triggerEvent(PygameInputHandler.inputEvents[InputEvent.LEFTUP])
                        PygameInputHandler.currentDown.remove(InputEvent.LEFTHELD)

        #for event in PygameInputHandler.currentDown:
        #    EventManager.triggerEvent(PygameInputHandler.inputEvents[event])

        EventManager.triggerEvent(PygameInputHandler.inputEvents[InputEvent.UPDATE])

    @staticmethod
    @override
    def getMousePosition() -> tuple[int, int]:
        return pg.mouse.get_pos()

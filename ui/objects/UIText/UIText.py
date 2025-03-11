import pygame as pg

from typing import override
from ui.objects import UIObject, UIObjectBody

def get_optimal_font_size(max_size: tuple[int, int], sysfont_name: str, text: str) -> int:
    
    def text_fits_in_box(max_size: tuple[int, int], text_size: tuple[int, int]) -> bool:
        return (max_size[0] > text_size[0]) and (max_size[1] > text_size[1])

    start_search: int = 0
    end_search: int = min(max_size)
    while start_search < end_search:
        mid_search: int = int((start_search + end_search) / 2)
        
        test_font: pg.font.Font = pg.font.SysFont(sysfont_name, mid_search)
        test_render: pg.Surface = test_font.render(text, False, 'white')
        test_size: tuple[int, int] = test_render.get_size()

        if text_fits_in_box(max_size, test_size):
            start_search = mid_search + 1
        else: 
            end_search = mid_search - 1

    return start_search


class UIDynamicTextCore(UIObject):
    
    content: str
    font: pg.font.Font
    font_name: str
    font_color: str

    def __init__(self, body: UIObjectBody, content: str, sysfont_name: str, font_color: str = 'white', active: bool = True) -> None:
        super().__init__(body, active)
        self.content = content
        self.updateFont(sysfont_name, font_color)

    def updateFont(self, sysfont_name: str = '', font_color: str = '') -> None:
        if sysfont_name == '':
            sysfont_name = self.font_name
        if font_color == '':
            font_color = self.font_color
        self.font_name = sysfont_name
        self.font_color = font_color
        self.font = pg.font.SysFont(sysfont_name, get_optimal_font_size(self.getSize(), sysfont_name, self.content))

    def updateContent(self, content: str) -> None:
        self.content = content
        self.updateFont()

    def update(self) -> None:
        super().update() #updates object body
        self.updateFont()


class UIDynamicText(UIDynamicTextCore):
    def __init__(self, body: UIObjectBody, content: str, sysfont_name: str, font_color: str = 'white', active: bool = True) -> None:
        super().__init__(body, content, sysfont_name, font_color, active)


class UITextCore(UIObject):
    
    content: str
    font: pg.font.Font
    font_color: str

    def __init__(self, body: UIObjectBody, content: str, font: pg.font.Font, font_color: str = 'white', active: bool = True) -> None:
        super().__init__(body, active)
        self.content = content
        self.font = font
        self.font_color = font_color

    def setFont(self, font: pg.font.Font, font_color: str = '') -> None:
        self.font_color = font_color
        self.font = font

    def updateContent(self, content: str) -> None:
        self.content = content

    def update(self) -> None:
        super().update() #updates object body


class UIText(UITextCore):
    def __init__(self, body: UIObjectBody, content: str, font: pg.font.Font, font_color: str = 'white', active: bool = True) -> None:
        super().__init__(body, content, font, font_color, active)

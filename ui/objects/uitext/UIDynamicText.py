from typing import override

from ..idrawer import UISurface
from ..generic import Color
from ..UIRenderer import UIRenderer
from ..uistyle import UIStyleElements

from .UIABCText import UIABCTextRenderer
from .UIText import UIText


def get_maximal_font_size(max_size: tuple[int, int], sysfont_name: str, text: str) -> int:
    
    def text_fits_in_box(max_size: tuple[int, int], text_size: tuple[int, int]) -> bool:
        return (max_size[0] > text_size[0]) and (max_size[1] > text_size[1])

    start_search: int = 0
    end_search: int = min(max_size)
    while start_search < end_search:
        mid_search: int = int((start_search + end_search) / 2)
        
        test_font = UIRenderer.font.SysFont(sysfont_name, mid_search)
        test_render: UISurface = test_font.render(text, (255, 255, 255))
        test_size: tuple[int, int] = test_render.getSize()

        if text_fits_in_box(max_size, test_size):
            start_search = mid_search + 1
        else: 
            end_search = mid_search - 1

    return start_search



class UIDynamicTextRenderer(UIABCTextRenderer):
    """
    UIDynamicTextRender is a UITextRender which dynamically scales the fontsize
    with the box-size, text-length and font type.
    """

    def __init__(self, body: UIText,
                       fontName: str='Arial', fontColor: Color=Color('white'),
                       active: bool=True) -> None:
        """
        __init__ initializes the UIDynamicTextRender instance

        Args:
            body: UIText = the refering UIText
            fontName: str = the systemfont name of used font
            fontColor: Color = the color the font should have
            active: bool = the active-state of the UIDynamicTextRenderer
        """
        self.active = active
        self.body = body

        self.fontName = fontName
        self.fontColor = fontColor

        self.updateFont()

    @override
    def updateFont(self) -> None:
        """
        updateFont updates the font of the UIDynamicTextRender used for render
        depending on the text-content, box-size and font type.
        """
        content = self.getUIObject().getContent()
        self.font = UIRenderer.font.SysFont(self.fontName, get_maximal_font_size(self.body.getSize(), self.fontName, content))


    @override
    def render(self, surface: UISurface) -> None:
        """
        render renders the UIObject onto the given surface

        Args:
            surface: UISurface = the surface the UIObject should be drawn on
        """

        # check if UIElement should be rendered
        if not self.active:
            return


        UIRenderer.getRenderStyle().getStyleElement(UIStyleElements.BASIC_RECT).render(UIRenderer.getDrawer(), surface, self.getUIObject().getRect())


        text_render: UISurface = self.font.render(self.getUIObject().getContent(), self.fontColor)
        text_size: tuple[int, int] = text_render.getSize()
        text_position: tuple[int, int] = (int(self.getUIObject().getPosition()[0] + (self.getUIObject().getSize()[0] - text_size[0]) / 2),
                                              int(self.getUIObject().getPosition()[1] + (self.getUIObject().getSize()[1] - text_size[1]) / 2))
        surface.blit(text_render, text_position)


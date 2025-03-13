from enum import Enum
from typing import Callable

from .generic import Color, Rect
from .UIABCRender import UIABCRender
from .idrawer import UISurface, UIFont, UISurfaceDrawer
from .uibutton import UIABCButtonRender, CycleButtonRenderStyle, UICycleButtonRender
from .uiobject import UIABCObjectRender
from .uitext import UIABCTextRender


class UIStyle(Enum):
    MOON = 0


class UIRenderer:
    

    drawer: UISurfaceDrawer
    renderstyle: UIStyle


    def __init__(self, drawer: UISurfaceDrawer, font: UIFont, renderstyle: UIStyle = UIStyle.MOON) -> None:
        self.drawer = drawer
        self.renderstyle = renderstyle
        UIRenderer.font = font

    def render(self, screen: UISurface, uiobjects: list[UIABCRender]) -> None:
        match self.renderstyle:
            case UIStyle.MOON:
                for uiobject in uiobjects:
                    self.renderMoon(screen, uiobject)

    def renderMoon(self, screen: UISurface, uiobject: UIABCRender) -> None:
        left, top = uiobject.getPosition()
        width, height = uiobject.getSize()
        right, bottom = left + width, top + height

        if isinstance(uiobject, UIABCButtonRender):
            self.renderButton(screen, uiobject, Color('white'))
        
        #render text
        if isinstance(uiobject, UIABCTextRender):
            self.renderText(screen, uiobject)
        
        #render border
        if isinstance(uiobject, UIABCObjectRender):
            borders: tuple[bool, bool, bool, bool] | bool = uiobject.getUIRenderInfo().borders
            if isinstance(borders, bool):
                borders = (borders, borders, borders, borders)
            
            if borders[0]:
                self.drawer.drawline(screen, (left, top), (right, top), (255,255,255))
            if borders[1]:
                self.drawer.drawline(screen, (left, top), (left, bottom), (255,255,255)) 
            if borders[2]:
                self.drawer.drawline(screen, (right, top), (right, bottom), (255,255,255))
            if borders[3]:
                self.drawer.drawline(screen, (left, bottom), (right, bottom), (255,255,255))


    def renderText(self, screen: UISurface, text: UIABCTextRender) -> None:
            text_render: UISurface = text.getUIRenderInfo().font.render(text.getUIObject().getContent(), text.getUIRenderInfo().fontColor)
            text_size: tuple[int, int] = text_render.getSize()
            text_position: tuple[int, int] = (int(text.getPosition()[0] + (text.getSize()[0] - text_size[0]) / 2),
                                              int(text.getPosition()[1] + (text.getSize()[1] - text_size[1]) / 2))
            
            screen.blit(text_render, text_position)


    def renderButton(self, screen: UISurface, button: UIABCButtonRender, color: Color) -> None:
        left, top = button.getPosition()
        width, height = button.getSize()

        def fill_with_lines(screen: UISurface, rect: Rect,
                            line_function: Callable[[int], int], line_spacing: float, draw: bool = True) -> tuple[tuple[int, int], tuple[int, int]]:
            """
            Returns:
                tuple[
                    tuple[int, int],
                    tuple[int, int]
                ]: start_point and end_point of first drawn line
            """

            def find_y_intersect(f: Callable[[int], int], y: int) -> int:
                iterations: int = 10
                cx: int = 0
                while iterations > 0:
                    cy: int = f(cx)
                    cya: int = f(cx + 1)
                    if cy == cya:
                        cx += 1
                    else:
                        cx += (y - f(cx)) // (f(cx+1) - f(cx))
                    iterations -= 1
                return cx

            first_start_point: tuple[int, int] = (-1, -1)
            first_end_point: tuple[int, int] = (-1, -1)

            actual_line_amount: int = int((rect.height + rect.width)/line_spacing) #-1 ?
            for line_number in range(-actual_line_amount, actual_line_amount + 1):
                cline_f: Callable[[int], int] = lambda x: line_function(x - rect.left) + int(rect.top + line_number * line_spacing)

                # calculate start point
                start_pointX: int
                start_pointY: int = int(rect.top + line_number * line_spacing)
                if start_pointY < rect.top:
                    start_pointX = find_y_intersect(cline_f, rect.top)
                elif start_pointY > rect.bottom:
                    start_pointX = find_y_intersect(cline_f, rect.bottom)
                else:
                    start_pointX = rect.left
                start_point: tuple[int, int] = (start_pointX, cline_f(start_pointX))

                # calculate end point
                end_pointX: int = rect.right
                end_pointY: int = cline_f(end_pointX)
                if end_pointY < rect.top:
                    end_pointX = find_y_intersect(cline_f, rect.top)
                elif end_pointY > rect.bottom:
                    end_pointX = find_y_intersect(cline_f, rect.bottom)
                else:
                    end_pointX = rect.right
                end_point: tuple[int, int] = (end_pointX, cline_f(end_pointX))

                if start_pointX >= rect.left and end_pointX <= rect.right and start_pointX < end_pointX:
                    nonlocal color
                    
                    if draw:
                        self.drawer.drawline(screen, start_point, end_point, color)

                    if first_start_point[0] == -1:
                        first_start_point = start_point
                        first_end_point = end_point

            return (first_start_point, first_end_point)
        if isinstance(button, UICycleButtonRender):
            line_amount: int = min(10, int(height / 10))
            line_spacing: float = height / (line_amount + 1)
            match button.getUIRenderInfo().renderStyle:
                case CycleButtonRenderStyle.DEFAULT:
                    pass
                case CycleButtonRenderStyle.PLAIN:
                    pass
                case CycleButtonRenderStyle.FILLING_HORIZONTAL:
                    activation_percent: float = button.getUIObject().currentState / (button.getUIObject().numberOfStates - 1)
                    activation_width: int = int(width * activation_percent)
                    fill_with_lines(screen, Rect((left, top), (activation_width, height)), lambda x: x, line_spacing)
                    fill_with_lines(screen, Rect((left, top), (activation_width, height)), lambda x: -x, line_spacing)
                case CycleButtonRenderStyle.FILLING_DIAGONAL:
                    activation_percent: float = button.getUIObject().currentState / (button.getUIObject().numberOfStates - 1)
                    activation_width: int = int(width * activation_percent)
                    fill_with_lines(screen, Rect((left, top), (activation_width, height)), lambda x: x, line_spacing)
                case CycleButtonRenderStyle.FILLING_DIAGONALALT:
                    state_percent: float = 1 / (button.getUIObject().numberOfStates - 1)
                    state_width: int = int(width * state_percent)

                    sign: bool = True
                    # vertical offset to align the diagonal lines vertically
                    p_end_point: tuple[int, int] = fill_with_lines(screen, Rect((0, top), (state_width, height)), lambda x: x, line_spacing, draw=False)[1]
                    p_start_point: tuple[int, int] = fill_with_lines(screen, Rect((0, top), (state_width, height)), lambda x: -x, line_spacing, draw=False)[0]
                    vertical_offset: int = p_end_point[1] - p_start_point[1]

                    for cs in range(1, button.getUIObject().currentState + 1):
                        state_left: int = left + (cs - 1) * state_width
                        if sign:
                            fill_with_lines(screen, Rect((state_left, top), (state_width, height)), lambda x: x, line_spacing)
                        else:
                            fill_with_lines(screen, Rect((state_left, top), (state_width, height)), lambda x: -x + vertical_offset, line_spacing)
                        sign = not sign
        

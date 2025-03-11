from enum import Enum
from typing import Callable
import pygame as pg

from ui.objects import DynamicCycleState, UIButton
from ui.objects import UIObject
from ui.objects import UIDynamicText, UIText

class UIStyle(Enum):
    MOON = 0

class ButtonRenderStyle(Enum):
    DEFAULT = 0
    PLAIN = 1
    FILLING_HORIZONTAL = 2
    FILLING_DIAGONAL = 3
    FILLING_DIAGONALALT = 4

class UIRenderer:
    
    renderstyle: UIStyle
    buttonrenderstyle: ButtonRenderStyle

    def __init__(self, renderstyle: UIStyle = UIStyle.MOON,
                 buttonrenderstyle: ButtonRenderStyle = ButtonRenderStyle.DEFAULT) -> None:
        self.renderstyle = renderstyle
        self.buttonrenderstyle = buttonrenderstyle

    def render(self, screen: pg.Surface, uiobjects: list[UIObject]) -> None:
        match self.renderstyle:
            case UIStyle.MOON:
                for uiobject in uiobjects:
                    self.renderMoon(screen, uiobject)

    def renderMoon(self, screen: pg.Surface, uiobject: UIObject) -> None:
        left, top = uiobject.getPosition()
        width, height = uiobject.getSize()
        right, bottom = left + width, top + height

        if isinstance(uiobject, UIButton):
            # shrink toggle button when pressed
            if isinstance(uiobject.button_state, DynamicCycleState) and uiobject.button_state.state == 1 and uiobject.button_state.max_state == 1:
                activation_decrement: float = 0.1
                left += int((activation_decrement / 2) * width)
                right -= int((activation_decrement / 2) * width)
                width = int(width * (1 - activation_decrement))
                top += int((activation_decrement / 2) * height)
                bottom -= int((activation_decrement / 2) * height)
                height = int(height * (1 - activation_decrement))

            self.renderButton(screen, uiobject, pg.Color('white'))
        
        #render border
        pg.draw.line(screen, 'white', (left, top), (right, top))
        pg.draw.line(screen, 'white', (left, top), (left, bottom)) 
        pg.draw.line(screen, 'white', (right, top), (right, bottom))
        pg.draw.line(screen, 'white', (left, bottom), (right, bottom))

        #render text
        if isinstance(uiobject, (UIText, UIDynamicText)):
            text_render: pg.Surface = uiobject.font.render(uiobject.content, True, uiobject.font_color)
            text_size: tuple[int, int] = text_render.get_size()
            text_position: tuple[int, int] = (int(left + (width - text_size[0]) / 2),
                                              int(top + (height - text_size[1]) / 2))
            
            screen.blit(text_render, text_position)

    def renderButton(self, screen: pg.Surface, button: UIButton, color: pg.Color) -> None:
        left, top = button.getPosition()
        width, height = button.getSize()

        def fill_with_lines(screen: pg.Surface, rect: pg.Rect, line_function: Callable[[int], int], line_spacing: float, draw: bool = True) -> tuple[tuple[int, int], tuple[int, int]]:
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
                        pg.draw.line(screen, color, start_point, end_point)

                    if first_start_point[0] == -1:
                        first_start_point = start_point
                        first_end_point = end_point

            return (first_start_point, first_end_point)
        
        match self.buttonrenderstyle:
            case ButtonRenderStyle.DEFAULT:
                pass
            case ButtonRenderStyle.PLAIN:
                pass
            case ButtonRenderStyle.FILLING_HORIZONTAL:
                if isinstance(button.button_state, DynamicCycleState):
                    line_amount: int = min(10, int(height / 10))
                    line_spacing: float = height / (line_amount + 1)
                    activation_percent: float = button.button_state.state / button.button_state.max_state
                    activation_width: int = int(width * activation_percent)
                    fill_with_lines(screen, pg.Rect((left, top), (activation_width, height)), lambda x: x, line_spacing)
                    fill_with_lines(screen, pg.Rect((left, top), (activation_width, height)), lambda x: -x, line_spacing)
            case ButtonRenderStyle.FILLING_DIAGONAL:
                if isinstance(button.button_state, DynamicCycleState):
                    line_amount: int = min(10, int(height / 10))
                    line_spacing: float = height / (line_amount + 1)
                    activation_percent: float = button.button_state.state / button.button_state.max_state
                    activation_width: int = int(width * activation_percent)
                    fill_with_lines(screen, pg.Rect((left, top), (activation_width, height)), lambda x: x, line_spacing)
            case ButtonRenderStyle.FILLING_DIAGONALALT:
                if isinstance(button.button_state, DynamicCycleState):
                    line_amount: int = min(10, int(height / 10))
                    line_spacing: float = height / (line_amount + 1)
                    state_percent: float = 1 / button.button_state.max_state
                    state_width: int = int(width * state_percent)
                    
                    sign: bool = True
                    # vertical offset to align the diagonal lines vertically
                    p_end_point: tuple[int, int] = fill_with_lines(screen, pg.Rect((0, top), (state_width, height)), lambda x: x, line_spacing, draw=False)[1]
                    p_start_point: tuple[int, int] = fill_with_lines(screen, pg.Rect((0, top), (state_width, height)), lambda x: -x, line_spacing, draw=False)[0]
                    vertical_offset: int = p_end_point[1] - p_start_point[1]

                    for cs in range(1, button.button_state.state + 1):
                        state_left: int = left + (cs - 1) * state_width
                        if sign:
                            fill_with_lines(screen, pg.Rect((state_left, top), (state_width, height)), lambda x: x, line_spacing)
                        else:
                            fill_with_lines(screen, pg.Rect((state_left, top), (state_width, height)), lambda x: -x + vertical_offset, line_spacing)
                        sign = not sign
        

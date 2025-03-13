
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, override

from ui.responsiveness import EventManager
from ..idrawer import UISurface
from ..generic import Rect
from ..uiobjectbody import UIABCBody
from ..uiobject import UIABCObject
from .UIABCClickButton import UIABCClickButton

class UICycleButton(UIABCClickButton):
    """
    UICycleButton is a implementation of UIABCClickButton where
    the button cycles between a fixed amount of states when clicked.
    """

    buttonEvents: list[str]
    numberOfStates: int
    currentState: int

    def __init__(self, objectBody: UIABCBody, numberOfStates: int=2, startState: int=0, buttonActive: bool=True) -> None:
        """
        __init__ initializes the UICycleButton instance

        Args:
            objectBody: UIABCBody = the body of the UICycleButton
            numberOfStates: int = the number of states of the button (min 2)
            startState: int = the startState of the UICycleButton (min 0, max numberOfState - 1)
            buttonActive: bool = boolean if the UICycleButton starts active
        """
        self.body = objectBody
        UIABCObject.update(self) #explicitly calls the update function from UIObject (in case it gets overwritten)

        self.numberOfStates = max(2, numberOfStates)
        self.currentState = min(self.numberOfStates - 1, max(0, startState))
        self.buttonActive = buttonActive
        
        self.buttonEvents = [EventManager.createEvent() for _ in range(numberOfStates)]

    @override
    def _trigger(self) -> None:
        """
        trigger gets called when the UIButton is triggered.
        For UICycleButton the currentState of the Butten gets incremented 
        (and wraps around if it reaches maxState).
        """
        EventManager.triggerEvent(self.buttonEvents[self.currentState])
        self.currentState = (self.currentState + 1) % self.numberOfStates

    def subscribeToButtonEvent(self, state: int, f: Callable, *args: Any) -> bool:
        """
        subscribeToButtonEvent subscribes a Callback to the triggerEvent of the
        given buttonState of the UICycleButton.

        Args:
            state: int = the buttonState the Callback should be subscribed to
            f: Callable = the function that should be subscribed
            *args: Any = the potential arguments the function needs

        Returns:
            bool = returns if the subscription was successful
        """
        if state >= 0 and state < self.numberOfStates:
            return EventManager.subscribeToEvent(self.buttonEvents[state], f, *args)
        return False

    def subscribeToButtonClick(self, f: Callable, *args: Any) -> bool:
        """
        subscribeToButtonClick subscribes a Callback to the triggerEvent of
        all buttonStates of the UICycleButton.

        Args:
            f: Callable = the function that should be subscribed
            *args: Any = the potential arguments the function needs

        Returns:
            bool = returns if the subscriptions were successful
        """
        return all([EventManager.subscribeToEvent(self.buttonEvents[x], f, *args) for x in range(self.numberOfStates)])
 

from .UIABCButton import UIABCButtonRenderer
from ..UIRenderer import UIRenderer
from ..uistyle import UIStyleElements
from ..UIABCRenderer import UIABCRenderer

class CycleButtonRenderStyle(Enum):
    """
    CycleButtonRenderStyle defines some renderStyles for the UICycleButtonRender.
    """
    DEFAULT = 0
    PLAIN = 1
    FILLING_HORIZONTAL = 2
    FILLING_DIAGONAL = 3
    FILLING_DIAGONALALT = 4

class UICycleButtonRenderer(UIABCButtonRenderer[UICycleButton]):
    """
    UICycleButtonRender is a UIButtonRender which uses UICycleButtonRenderInfo to
    render the UICycleButton.
    """
    buttonRenderStyle: CycleButtonRenderStyle

    def __init__(self, body: UICycleButton, 
                       buttonRenderStyle: CycleButtonRenderStyle=CycleButtonRenderStyle.FILLING_DIAGONALALT, 
                       active: bool=True) -> None:
        """
        __init__ initializes the UICycleButtonRender instance

        Args:
            body: UICycleButton = the refering UICycleButton
            renderInfo: UICycleButtonRenderInfo = the UIRenderInfo used for rendering the UICycleButtonRender
        """
        self.active = active
        self.body = body
        
        self.buttonRenderStyle = buttonRenderStyle

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

        color: str = 'white'

        rect: Rect = self.getUIObject().getRect()

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
                        UIRenderer.drawer.drawline(screen, start_point, end_point, color)

                    if first_start_point[0] == -1:
                        first_start_point = start_point
                        first_end_point = end_point

            return (first_start_point, first_end_point)

            
        line_amount: int = min(10, int(rect.height / 10))
        line_spacing: float = rect.height / (line_amount + 1)
        
        match self.buttonRenderStyle:
            case CycleButtonRenderStyle.DEFAULT:
                pass

            case CycleButtonRenderStyle.PLAIN:
                pass

            case CycleButtonRenderStyle.FILLING_HORIZONTAL:
                activation_percent: float = self.getUIObject().currentState / (self.getUIObject().numberOfStates - 1)
                activation_width: int = int(rect.width * activation_percent)
                fill_with_lines(surface, Rect(rect.getPosition(), (activation_width, rect.height)), lambda x: x, line_spacing)
                fill_with_lines(surface, Rect(rect.getPosition(), (activation_width, rect.height)), lambda x: -x, line_spacing)

            case CycleButtonRenderStyle.FILLING_DIAGONAL:
                activation_percent: float = self.getUIObject().currentState / (self.getUIObject().numberOfStates - 1)
                activation_width: int = int(rect.width * activation_percent)
                fill_with_lines(surface, Rect(rect.getPosition(), (activation_width, rect.height)), lambda x: x, line_spacing)

            case CycleButtonRenderStyle.FILLING_DIAGONALALT:
                state_percent: float = 1 / (self.getUIObject().numberOfStates - 1)
                state_width: int = int(rect.width * state_percent)

                sign: bool = True
                # vertical offset to align the diagonal lines vertically
                p_end_point: tuple[int, int] = fill_with_lines(surface, Rect((0, rect.top), (state_width, rect.height)), lambda x: x, line_spacing, draw=False)[1]
                p_start_point: tuple[int, int] = fill_with_lines(surface, Rect((0, rect.top), (state_width, rect.height)), lambda x: -x, line_spacing, draw=False)[0]
                vertical_offset: int = p_end_point[1] - p_start_point[1]

                for cs in range(1, self.getUIObject().currentState + 1):
                    state_left: int = rect.left + (cs - 1) * state_width
                    if sign:
                        fill_with_lines(surface, Rect((state_left, rect.top), (state_width, rect.height)), lambda x: x, line_spacing)
                    else:
                        fill_with_lines(surface, Rect((state_left, rect.top), (state_width, rect.height)), lambda x: -x + vertical_offset, line_spacing)
                    sign = not sign
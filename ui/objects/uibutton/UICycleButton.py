
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, override

from ui.responsiveness import EventManager
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
 

from .UIABCButton import UIABCButtonRenderInfo, UIABCButtonRender
from ..UIABCRender import UIABCRender

class CycleButtonRenderStyle(Enum):
    """
    CycleButtonRenderStyle defines some renderStyles for the UICycleButtonRender.
    """
    DEFAULT = 0
    PLAIN = 1
    FILLING_HORIZONTAL = 2
    FILLING_DIAGONAL = 3
    FILLING_DIAGONALALT = 4

@dataclass
class UICycleButtonRenderInfo(UIABCButtonRenderInfo):
    """
    UICycleButtonRenderInfo is the UIRenderInfo for the UICycleButtonRender
    """
    renderStyle: CycleButtonRenderStyle = CycleButtonRenderStyle.FILLING_DIAGONALALT

class UICycleButtonRender(UIABCButtonRender[UICycleButton, UICycleButtonRenderInfo]):
    """
    UICycleButtonRender is a UIButtonRender which uses UICycleButtonRenderInfo to
    render the UICycleButton.
    """

    def __init__(self, body: UICycleButton, renderInfo: UICycleButtonRenderInfo) -> None:
        """
        __init__ initializes the UICycleButtonRender instance

        Args:
            body: UICycleButton = the refering UICycleButton
            renderInfo: UICycleButtonRenderInfo = the UIRenderInfo used for rendering the UICycleButtonRender
        """
        self.body = body
        self.renderInfo = renderInfo


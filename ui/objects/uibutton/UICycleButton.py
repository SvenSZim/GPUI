
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, override

from ui.responsiveness import EventManager
from ..uiobjectbody import UIABCBody
from ..uiobject import UIABCObject
from .UIABCClickButton import UIABCClickButton

class UICycleButton(UIABCClickButton):

    buttonEvents: list[str]
    numberOfStates: int
    currentState: int


    def __init__(self, objectBody: UIABCBody, numberOfStates: int=2, startState: int=0, active: bool=True) -> None:
        self.active = active
        self.body = objectBody
        UIABCObject.update(self) #explicitly calls the update function from UIObject (in case it gets overwritten)

        self.numberOfStates = numberOfStates
        self.currentState = startState
        
        self.buttonEvents = [EventManager.createEvent() for _ in range(numberOfStates)]

    @override
    def trigger(self) -> None:
        EventManager.triggerEvent(self.buttonEvents[self.currentState])
        self.currentState = (self.currentState + 1) % self.numberOfStates

    @override
    def addGlobalTriggerEvent(self, event: str) -> bool:
        return EventManager.subscribeToEvent(event, UICycleButton.trigger, self)

    def subscribeToButtonEvent(self, f: Callable, *args: Any) -> bool:
        return all([EventManager.subscribeToEvent(self.buttonEvents[x], f, *args) for x in range(self.numberOfStates)])
 

from .UIABCButton import UIABCButtonRenderInfo, UIABCButtonRender
from ..UIABCRender import UIABCRender

class CycleButtonRenderStyle(Enum):
    DEFAULT = 0
    PLAIN = 1
    FILLING_HORIZONTAL = 2
    FILLING_DIAGONAL = 3
    FILLING_DIAGONALALT = 4

@dataclass
class UICycleButtonRenderInfo(UIABCButtonRenderInfo):
    renderStyle: CycleButtonRenderStyle = CycleButtonRenderStyle.FILLING_DIAGONALALT

class UICycleButtonRender(UIABCButtonRender[UICycleButton, UICycleButtonRenderInfo]):

    def __init__(self, body: UICycleButton, renderInfo: UICycleButtonRenderInfo) -> None:
        self.body = body
        self.renderInfo = renderInfo


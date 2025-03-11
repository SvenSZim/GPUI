from abc import abstractmethod
from enum import Enum
from typing import Any, Callable, Protocol

from ui.objects import UIObject, UIObjectBody
from ui.responsiveness import EventManager

def collidepoint(topleft: tuple[int, int], size: tuple[int, int], point: tuple[int, int]) -> bool:
    x, y = topleft
    w, h = size
    px, py = point
    return px > x and py > y and px < x + w and py < y + h

class UIButtonCore(UIObject):

    button_event: str

    def __init__(self, body: UIObjectBody, active: bool = True) -> None:
        super().__init__(body, active)
        self.button_event = EventManager.createEvent()

    def addTriggerEvent(self, event: str) -> bool:
        return EventManager.subscribeToEvent(event, UIButtonCore.testForClickIntersect, self)

    def addGlobalTriggerEvent(self, event: str) -> bool:
        return EventManager.subscribeToEvent(event, EventManager.triggerEvent, self.button_event)

    def subscribeToButtonEvent(self, f: Callable, *args: Any) -> bool:
        return EventManager.subscribeToEvent(self.button_event, f, *args)

    def testForClickIntersect(self, mouseposition: tuple[int, int]):
        if collidepoint(self.getPosition(), self.getSize(), mouseposition):
            EventManager.triggerEvent(self.button_event)

class ButtonState(Protocol):
    @abstractmethod
    def reset(self) -> 'ButtonState':
        pass

    @abstractmethod
    def switch(self) -> 'ButtonState':
        pass

class SwitchState(Enum):
    OFF=0
    ON=1

    def restet(self) -> 'SwitchState':
        return SwitchState.OFF

    def switch(self) -> 'SwitchState':
        return {SwitchState(x): SwitchState((x+1) % 2) for x in range(2)}[self]

class DynamicCycleState(ButtonState):
    state: int
    max_state: int

    def __init__(self, state: int, max_state: int):
        self.state = state
        self.max_state = max_state

    def reset(self) -> 'DynamicCycleState':
        return DynamicCycleState(0, self.max_state)

    def switch(self) -> 'DynamicCycleState':
        next_state: int = (self.state + 1) % (self.max_state + 1)
        return DynamicCycleState(next_state, self.max_state)

    def __repr__(self) -> str:
        return f"IncState.s{self.state}"

class UIButton(UIButtonCore):

    button_state: ButtonState

    def __init__(self, body: UIObjectBody, button_state: ButtonState = DynamicCycleState(0, 5), active: bool = True) -> None:
        super().__init__(body, active)
        self.button_state = button_state
        self.subscribeToButtonEvent(self.switch)

    def switch(self) -> None:
        self.button_state = self.button_state.switch()

    def reset(self) -> None:
        self.button_state = self.button_state.reset()

    def addGlobalResetEvent(self, event: str) -> bool:
        return EventManager.subscribeToEvent(event, UIButton.reset, self)



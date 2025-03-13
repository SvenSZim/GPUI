from abc import ABC
from typing import override

from ui.responsiveness import EventManager, InputManager
from .UIABCButton import UIABCButton


def collidepoint(topleft: tuple[int, int], size: tuple[int, int], point: tuple[int, int]) -> bool:
    x, y = topleft
    w, h = size
    px, py = point
    return px > x and py > y and px < x + w and py < y + h


class UIABCClickButton(UIABCButton, ABC):
    
    def testForClickIntersect(self):
        if collidepoint(self.getPosition(), self.getSize(), InputManager.getMousePosition()):
            self.trigger()

    @override
    def addTriggerEvent(self, event: str) -> bool:
        return EventManager.subscribeToEvent(event, UIABCClickButton.testForClickIntersect, self)

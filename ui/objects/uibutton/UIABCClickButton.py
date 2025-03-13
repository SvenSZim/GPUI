from abc import ABC
from typing import override

from ui.responsiveness import EventManager, InputManager
from .UIABCButton import UIABCButton


class UIABCClickButton(UIABCButton, ABC):
    """
    UIABCClickButton is the abstract base class for all UIClickButtons
    (which are clickable buttons).
    """
    
    @override
    def _activeTrigger(self):
        """
        activeTrigger is the default function to call when trying to trigger the
        button. It checks if the button is active and the mousecursor being inside
        the button rect before calling the true trigger.
        """
        if self.getButtonActive() and self.getRect().collidepoint(InputManager.getMousePosition()):
            self._trigger()

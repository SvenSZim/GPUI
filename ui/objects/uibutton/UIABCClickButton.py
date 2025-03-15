from abc import ABC
from typing import override

from ui.responsiveness import InputManager
from ..generic import Rect
from ..uiobjectbody import UIABCBody
from .UIABCButton import UIABCButton


class UIABCClickButton(UIABCButton, ABC):
    """
    UIABCClickButton is the abstract base class for all UIClickButtons
    (which are clickable buttons).
    """

    def __init__(self, body: UIABCBody | Rect, buttonActive: bool=True) -> None:
        """
        __init__ initializes the UIABCClickButton values for the UIButtonElement

        Args:
            body: UIABCBody = the body of the UIButtonElement (for UIABCButton)
            buttonActive: bool = the button active-state (for UIABCButton)
        """
        super().__init__(body, buttonActive)
    
    @override
    def _activeTrigger(self):
        """
        activeTrigger is the default function to call when trying to trigger the
        button. It checks if the button is active and the mousecursor being inside
        the button rect before calling the true trigger.
        """
        if self._buttonActive and self.getRect().collidepoint(InputManager.getMousePosition()):
            self._trigger()

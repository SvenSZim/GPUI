from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar

from ui.responsiveness import EventManager
from ..uiobject import UIABCObject



class UIABCButton(UIABCObject, ABC):
    """
    UIABCButton is the abstract base class for all UIButtons
    """

    buttonActive: bool # button active-state

    def getButtonActive(self) -> bool:
        """
        getButtonActive returns the active-state of the UIButton

        Returns:
            bool = active-state of the UIButton
        """
        return self.buttonActive

    def toggleButtonActive(self) -> bool:
        """
        toggleButtonActive toggles the active-state of the UIButton

        Returns:
            bool = new active-state of the UIButton
        """
        self.buttonActive = not self.buttonActive
        return self.buttonActive

    def setButtonActive(self, buttonActive: bool) -> None:
        """
        setButtonActive sets the active-state of the UIButton

        Args:
            buttonActive: bool = new active-state of the UIButton
        """
        self.buttonActive = buttonActive
    
    @abstractmethod
    def _trigger(self) -> None:
        """
        trigger gets called when the UIButton is triggered.
        (probably triggers a buttonEvent)
        """
        pass

    def _activeTrigger(self) -> None:
        """
        activeTrigger is the default function to call when trying to trigger the
        button. It checks if the button is active before calling the true trigger.
        """
        if self.getButtonActive():
            self._trigger()

    def addTriggerEvent(self, event: str) -> bool:
        """
        addTriggerEvent adds a event which activates the button-check-for-trigger.
        (default: _activeTrigger)
        """
        return EventManager.subscribeToEvent(event, self._activeTrigger)

    def addGlobalTriggerEvent(self, event: str) -> bool:
        """
        addGlobalTriggerEvent adds a event which immediatly triggers the button.
        """
        EventManager.subscribeToEvent(event, UIABCButton._activeTrigger, self)
        


from ..uiobject import UIABCObjectRenderInfo, UIABCObjectRender

B = TypeVar('B', bound=UIABCButton)

@dataclass
class UIABCButtonRenderInfo(UIABCObjectRenderInfo):
    """
    UIABCButtonRenderInfo is the abstract base class for all UIButtonRenderInfo
    """
    pass

I = TypeVar('I', bound=UIABCButtonRenderInfo)

class UIABCButtonRender(UIABCObjectRender[B, I], ABC):
    """
    UIABCButtonRender is the abstract base class for all UIButtonRender
    """
    pass

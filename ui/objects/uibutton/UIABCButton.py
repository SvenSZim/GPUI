from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from ui.responsiveness import EventManager

from ..UIABC import UIABC
from ..UIABCRenderer import UIABCRenderer
from ..uiobjectbody import UIABCBody



class UIABCButton(UIABC[UIABCBody], ABC):
    """
    UIABCButton is the abstract base class for all UIButtons
    """

    _buttonActive: bool # button active-state

    def __init__(self, body: UIABCBody, buttonActive: bool=True) -> None:
        """
        __init__ initializes the UIABCButton values for the UIButtonElement

        Args:
            body: UIABCBody = the body of the UIButtonElement (for UIABC)
            buttonActive: bool = the button active-state
        """
        super().__init__(body)
        self._buttonActive = buttonActive

    def getButtonActive(self) -> bool:
        """
        getButtonActive returns the active-state of the UIButton

        Returns:
            bool = active-state of the UIButton
        """
        return self._buttonActive

    def toggleButtonActive(self) -> bool:
        """
        toggleButtonActive toggles the active-state of the UIButton

        Returns:
            bool = new active-state of the UIButton
        """
        self._buttonActive = not self._buttonActive
        return self._buttonActive

    def setButtonActive(self, buttonActive: bool) -> None:
        """
        setButtonActive sets the active-state of the UIButton

        Args:
            buttonActive: bool = new active-state of the UIButton
        """
        self._buttonActive = buttonActive
    
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



Core = TypeVar('Core', bound=UIABCButton)

class UIABCButtonRenderer(Generic[Core], UIABCRenderer[Core], ABC):
    """
    UIABCButtonRender is the abstract base class for all UIButtonRender
    """
    def __init__(self, core: Core, active: bool=True) -> None:
        """
        __init__ initializes the values of UIABCButtonRenderer for the UIButtonRenderer

        Args:
            core: Core (bound=UIABCButton) = the refering UIButtonElement of the UIButtonRenderer (for UIABCRenderer)
            active: bool = active-state of the UIButtonRenderer (for UIABCRenderer)
        """
        super().__init__(core, active)

from typing import override
from ....responsiveness import EventManager, InputManager, InputEvent
from ...generic import Rect
from ..uielementbody import UIABCBody, UIStaticBody
from ..UIABCCore import UIABCCore

class UIButtonCore(UIABCCore[UIABCBody]):

    __buttonActive: bool
    __buttonEvents: list[str]
    __numberOfStates: int
    __currentState: int

    def __init__(self, body: UIABCBody | Rect, numberOfStates: int=2, startState: int=0, buttonActive: bool=True) -> None:
        if isinstance(body, Rect):
            body = UIStaticBody(body)
        super().__init__(body)
        self.update()
        
        self.__buttonActive      = buttonActive
        self.__numberOfStates    = max(2, numberOfStates)
        self.__currentState      = min(0, max(self.__numberOfStates-1, startState))

        self.__buttonEvents = [EventManager.createEvent() for _ in range(self.__numberOfStates)]

        EventManager.subscribeToEvent(InputManager.getEvent(InputEvent.MOUSEBUTTONDOWN), UIButtonCore.activeTrigger, self)


    @override
    def update(self) -> None:
        self._body.update()
    
    def getNumberOfButtonStates(self) -> int:
        return self.__numberOfStates

    def getCurrentButtonState(self) -> int:
        return self.__currentState
    
    def getButtonActive(self) -> bool:
        """
        getButtonActive returns the active-state of the UIButton

        Returns:
            bool = active-state of the UIButton
        """
        return self.__buttonActive

    def toggleButtonActive(self) -> bool:
        """
        toggleButtonActive toggles the active-state of the UIButton

        Returns:
            bool = new active-state of the UIButton
        """
        self.__buttonActive = not self.__buttonActive
        return self.__buttonActive

    def setButtonActive(self, buttonActive: bool) -> None:
        """
        setButtonActive sets the active-state of the UIButton

        Args:
            buttonActive: bool = new active-state of the UIButton
        """
        self.__buttonActive = buttonActive
    
    def __trigger(self) -> None:
        """
        trigger gets called when the UIButton is triggered.
        """
        EventManager.triggerEvent(self.__buttonEvents[self.__currentState])
        self.__currentState = (self.__currentState + 1) % self.__numberOfStates

    def activeTrigger(self) -> None:
        """
        activeTrigger is the default function to call when trying to trigger the
        button. It checks if the button is active before calling the true trigger.
        """
        if self.__buttonActive and self._body.getRect().collidepoint(InputManager.getMousePosition()):
            self.__trigger()

    def addTriggerEvent(self, event: str) -> bool:
        """
        addTriggerEvent adds a event which activates the button-check-for-trigger.
        (default: _activeTrigger)
        """
        return EventManager.subscribeToEvent(event, self.activeTrigger)

    def globalTrigger(self) -> None:
        """
        activeTrigger is the default function to call when trying to trigger the
        button. It checks if the button is active before calling the true trigger.
        """
        if self.__buttonActive:
            self.__trigger()

    def addGlobalTriggerEvent(self, event: str) -> bool:
        """
        addGlobalTriggerEvent adds a event which immediatly triggers the button.
        """
        return EventManager.subscribeToEvent(event, UIButtonCore.globalTrigger, self)




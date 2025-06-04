from typing import Any, override

from ......utility      import Rect
from ......interaction  import Togglable
from ....element        import Element
from ..interactablecore import InteractableCore

class ElementCycleCore(InteractableCore, Togglable):
    """
    ElementCycleCore is the core object of the interactable 'ElementCycle'.
    """
    __cycleData: list[Element]

    def __init__(self, rect: Rect, *inner: Element, startState: int=0, buttonActive: bool=True) -> None:
        if not len(inner):
            raise ValueError('Cannot instantiate ElementCycle without inner elements!')
        self.__cycleData = list(inner)

        InteractableCore.__init__(self, rect)
        Togglable.__init__(self, numberOfStates=len(self.__cycleData), startState=startState, buttonActive=buttonActive)
        
        self.__alignInner()

    def getCurrentElement(self) -> Element:
        return self.__cycleData[self._currentState]

    def __alignInner(self) -> None:
        for el in self.__cycleData:
            el.align(self)
            el.alignSize(self)
    
    @override
    def getInnerSizing(self, elSize: tuple[int, int], args: dict[str, Any]) -> tuple[int, int]:
        maxX, maxY = 0, 0
        for el in self.__cycleData:
            cX, cY = el.getInnerSizing(elSize, args)
            if cX > maxX:
                maxX = cX
            if cY > maxY:
                maxY = cY
        return maxX, maxY

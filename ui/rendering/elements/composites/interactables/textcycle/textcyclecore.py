
from ......utility      import Rect
from ......interaction  import Togglable
from ..interactablecore import InteractableCore

class TextCycleCore(InteractableCore, Togglable):
    """
    TextCycleCore is the core object of the interactable 'TextCycle'.
    """
    __contents: list[str]
    def __init__(self, rect: Rect, contents: list[str], startState: int=0, buttonActive: bool=True) -> None:
        self.__contents = contents
        InteractableCore.__init__(self, rect)
        Togglable.__init__(self, numberOfStates=len(contents), startState=startState, buttonActive=buttonActive)

    def getContent(self) -> str:
        return self.__contents[self._currentState]

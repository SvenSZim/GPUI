
from ......interaction  import Togglable
from ....element        import Element
from ..interactablecore import InteractableCore

class TogglewrapperCore(InteractableCore, Togglable):
    """
    TogglewrapperCore is the core object of the interactable 'Togglewrapper'.
    """

    __inner: Element

    def __init__(self, inner: Element, numberOfStates: int, startState: int, buttonActive: bool=True) -> None:
        self.__inner = inner

        InteractableCore.__init__(self, self.__inner.getRect())
        Togglable.__init__(self, numberOfStates=numberOfStates, startState=startState, buttonActive=buttonActive)

        self.__inner.alignpoint(self)
        self.__inner.alignpoint(self, (1,1), (1,1), keepSize=False)

    def getInner(self) -> Element:
        return self.__inner

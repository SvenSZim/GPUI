from typing import override

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

        self.__inner.align(self)
        self.__inner.alignSize(self)

    def getInner(self) -> Element:
        return self.__inner

    @override
    def getInnerSizing(self, elSize: tuple[int, int]) -> tuple[int, int]:
        return self.__inner.getInnerSizing(elSize)

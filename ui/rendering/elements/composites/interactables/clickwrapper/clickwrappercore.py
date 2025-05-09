
from ......interaction  import Holdable
from ....element        import Element
from ..interactablecore import InteractableCore

class ClickwrapperCore(InteractableCore, Holdable):
    """
    ClickwrapperCore is the core object of the interactable 'Clickwrapper'.
    """

    __inner: Element

    def __init__(self, inner: Element, buttonActive: bool=True) -> None:
        self.__inner = inner

        InteractableCore.__init__(self, self.__inner.getRect())
        Holdable.__init__(self, buttonActive=buttonActive)

        self.__inner.align(self)
        self.__inner.alignSize(self)

    def getInner(self) -> Element:
        return self.__inner

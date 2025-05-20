from typing import Callable, Optional, override

from .....utility      import Rect
from ...element        import Element
from ..compositioncore import CompositionCore
from ..addons          import Stacked
from ..interactables   import Togglewrapper

class MultiselectCore(CompositionCore):
    """
    MultiselectCore is the core object of the interactable 'Multiselect'.
    """
    __state: int
    __restriction: Callable[[int], int]
    __innerSelectors: list[Togglewrapper]
    __inner: Stacked

    def __init__(self, rect: Rect, *inner: Element | tuple[Element, float], alignVertical: bool=True, offset: int=0,
                 startState: int=0x0, restriction: Optional[Callable[[int], int]]=None) -> None:
        if restriction is None:
            self.__restriction = lambda _: 2**len(inner) - 1
        else:
            self.__restriction = restriction
        self.__state = startState

        self.__innerSelectors = []
        innerSelectors: list[Togglewrapper | tuple[Togglewrapper, float]] = []
        for nr, el in enumerate(inner):
            if isinstance(el, Element):
                newSelector: Togglewrapper = Togglewrapper(el, startState=startState & (1 << nr), buttonActive=True)
                newSelector.quickSubscribeToClick(self.__selectorToggle, nr)
                innerSelectors.append(newSelector)
                self.__innerSelectors.append(newSelector)
            else:
                newSelector: Togglewrapper = Togglewrapper(el[0], startState=startState & (1 << nr), buttonActive=True)
                newSelector.quickSubscribeToClick(self.__selectorToggle, nr)
                innerSelectors.append((newSelector, el[1]))
                self.__innerSelectors.append(newSelector)

        self.__applyRestriction()
        self.__inner = Stacked(rect, rect, *innerSelectors, alignVertical=alignVertical, offset=offset)
        CompositionCore.__init__(self, self.__inner.getRect())

        self.__inner.align(self)
        self.__inner.alignSize(self)

    def getInner(self) -> Stacked:
        return self.__inner

    @override
    def getInnerSizing(self, elSize: tuple[int, int]) -> tuple[int, int]:
        return self.__inner.getInnerSizing(elSize)


    def __selectorToggle(self, selector: int) -> None:
        self.__state ^= (1 << selector)
        self.__applyRestriction()

    def __applyRestriction(self) -> None:
        restriction: int = self.__restriction(self.__state)
        for nr, selector in enumerate(self.__innerSelectors):
            selector.setButtonActive(bool(restriction & (1 << nr)))

    def setButtonActive(self, buttonActive: bool) -> None:
        for s in self.__innerSelectors:
            s.setButtonActive(buttonActive)

    def toggleButtonActive(self) -> bool:
        if len(self.__innerSelectors) == 0:
            return True
        a: bool = self.__innerSelectors[0].toggleButtonActive()
        self.setButtonActive(a)
        return a


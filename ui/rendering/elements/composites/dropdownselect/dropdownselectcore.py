
from typing import override
from .....utility      import Rect
from .....interaction  import Togglable, EventManager
from ...element        import Element
from ...atoms          import Box, BoxPrefab, Text, TextCO
from ..addons          import Framed, FramedPrefab, Dropdown
from ..compositioncore import CompositionCore
from ..interactables   import Clickwrapper

class DropdownselectCore(CompositionCore, Togglable):
    """
    DropdownselectCore is the core object of the interactable 'Dropdownselect'.
    """
    __innerSelectors: list[Clickwrapper]
    __outer: list[Element]
    __dropdown: Dropdown

    def __init__(self, rect: Rect, *inner: tuple[Element | tuple[Element, float], Element], verticalDropdown: bool=True, offset: int=0,
                 startState: int=0, buttonActive: bool=True) -> None:
        CompositionCore.__init__(self, rect)
        Togglable.__init__(self, numberOfStates=len(inner)+1, startState=startState, buttonActive=buttonActive)

        self.__innerSelectors = []
        innerSelectors: list[Clickwrapper | tuple[Clickwrapper, float]] = []
        self.__outer = [Framed(Text(rect, 'SELECT', renderData=[TextCO.COLOR1, TextCO.SIZE_M]), renderData=FramedPrefab.BORDERED)]
        for nr, (el, head) in enumerate(inner):
            if isinstance(el, Element):
                newSelector: Clickwrapper = Clickwrapper(el, buttonActive=False)
                newSelector.quickSubscribeToClick(self._onCustomTrigger, lambda _, k=nr+1: k)
                innerSelectors.append(newSelector)
                self.__innerSelectors.append(newSelector)
            else:
                newSelector: Clickwrapper = Clickwrapper(el[0], buttonActive=False)
                newSelector.quickSubscribeToClick(self._onCustomTrigger, lambda _, k=nr+1: k)
                innerSelectors.append((newSelector, el[1]))
                self.__innerSelectors.append(newSelector)

            self.__outer.append(head)
 
        for el in self.__outer:
            el.alignpoint(self)
            el.alignpoint(self, (1,1), (1,1), keepSize=False)

        self.__dropdown = Dropdown(Box(rect, renderData=BoxPrefab.INVISIBLE), *innerSelectors, verticalDropdown=verticalDropdown, offset=offset, dropdownActive=buttonActive)

        self.__dropdown.addGlobalTriggerEvent(self._onclick)

        for iS in innerSelectors:
            if isinstance(iS, Element):
                self.__dropdown.quickSubscribeToClick(iS.toggleButtonActive)
            else:
                self.__dropdown.quickSubscribeToClick(iS[0].toggleButtonActive)

        self.__dropdown.alignpoint(self)
        self.__dropdown.alignpoint(self, (1,1), (1,1), keepSize=False)
    
    def getOuter(self) -> Element:
        return self.__outer[self.getCurrentToggleState()]

    def getDropdown(self) -> Dropdown:
        return self.__dropdown
    


    @override
    def setButtonActive(self, buttonActive: bool) -> None:
        for s in self.__innerSelectors:
            s.setButtonActive(buttonActive)
        return super().setButtonActive(buttonActive)

    @override
    def toggleButtonActive(self) -> bool:
        a = super().toggleButtonActive()
        self.setButtonActive(a)
        return a


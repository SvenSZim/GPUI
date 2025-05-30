from typing import Any, Optional, override

from ......utility      import AlignType, Rect
from ......interaction  import Togglable
from ....element    import Element
from ..grouped      import Grouped
from ..addoncore    import AddonCore

class DropdownCore(AddonCore[Element], Togglable):
    """
    DropdownCore is the core object of the addon 'Dropdown'.
    """
    __inner: Grouped
    __offset: int
    __innercount: int
    __innersize: float
    __verticalDropdown: bool

    def __init__(self, head: Element, *inner: tuple[Element, float], verticalDropdown: bool=True, offset: int=0, buttonActive: bool=True) -> None:
        self.__offset = offset
        self.__innercount = len(inner)
        self.__innersize = sum([i[1] if isinstance(i, tuple) else 1.0 for i in inner])
        self.__verticalDropdown = verticalDropdown
        
        self.__inner = Grouped(Rect(), *inner, alignVertical=verticalDropdown, offset=offset)
        self.__inner.setActive(False)

        AddonCore.__init__(self, head.getRect(), head)
        Togglable.__init__(self, numberOfStates=2, buttonActive=buttonActive)

        self.quickSubscribeToToggleState(0, self.__inner.setActive, False)
        self.quickSubscribeToToggleState(1, self.__inner.setActive, True)
 
    def getDropdown(self) -> Optional[Element]:
        if self._currentState:
            return self.__inner

    @override
    def getInnerSizing(self, elSize: tuple[int, int], args: dict[str, Any]) -> tuple[int, int]:
        return self._inner.getInnerSizing(elSize)

    @override
    def _alignInner(self) -> None:
        self._inner.align(self)
        self._inner.alignSize(self)
        if self.__innercount == 0:
            return

        if self.__verticalDropdown:
            self.__inner.alignSize(self, relativeAlign=(1.0, self.__innersize), absoluteOffset=(0, self.__offset * (self.__innercount-1)))
            self.__inner.align(self, AlignType.BiL)
        else:
            self.__inner.alignSize(self, relativeAlign=(self.__innersize, 1.0), absoluteOffset=(self.__offset * (self.__innercount-1), 0))
            self.__inner.align(self, AlignType.iTR)

    @override
    def setActive(self, active: bool) -> None:
        self.setButtonActive(active)
        self.__inner.setActive(active and bool(self._currentState))

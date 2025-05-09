from typing import override

from ......utility      import AlignType
from ......interaction  import Togglable
from ....element import Element
from ..stacked   import Stacked
from ..addoncore import AddonCore

class DropdownCore(AddonCore, Togglable):
    """
    DropdownCore is the core object of the addon 'Dropdown'.
    """
    __outer: Element
    __verticalDropdown: bool
    def __init__(self, outer: Element, *inner: Element | tuple[Element, float], verticalDropdown: bool=True, offset: int=0, buttonActive: bool=True) -> None:
        
        self.__outer = outer
        self.__verticalDropdown = verticalDropdown
        
        mStack: Stacked = Stacked(outer.getRect(), outer.getRect(), *inner, alignVertical=verticalDropdown, offset=offset)
        AddonCore.__init__(self, outer.getRect(), mStack)
        Togglable.__init__(self, numberOfStates=2, buttonActive=buttonActive)
 
    def getOuter(self) -> Element:
        return self.__outer

    @override
    def _alignInner(self) -> None:
        self.__outer.align(self)
        self.__outer.alignSize(self)

        if self.__verticalDropdown:
            self._inner.alignSize(self, alignY=False)
            self._inner.align(self, AlignType.BM)
        else:
            self._inner.alignSize(self, alignX=False)
            self._inner.align(self, AlignType.MR)

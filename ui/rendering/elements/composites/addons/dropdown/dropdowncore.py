from typing import override

from ......utility      import Rect
from ......interaction  import Togglable
from ....body    import LayoutManager
from ....element import Element
from ..stack     import Stack
from ..addoncore import AddonCore

class DropdownCore(AddonCore, Togglable):
    """
    DropdownCore is the core object of the addon 'Dropdown'.
    """
    __verticalDropdown: bool
    def __init__(self, outer: Rect, *inner: Element | tuple[Element, float], verticalDropdown: bool=True, offset: int=0, buttonActive: bool=True) -> None:
        
        self.__verticalDropdown = verticalDropdown
        
        mStack: Stack = Stack(outer, outer, *inner, alignVertical=verticalDropdown, offset=offset)
        AddonCore.__init__(self, outer, mStack)
        Togglable.__init__(self, numberOfStates=2, buttonActive=buttonActive)

    
    @override
    def _alignInner(self) -> None:
        LayoutManager.addConnection((True, True), self._inner.getCore().getBody(), self.getBody(), (0.0, 0.0), (0.0, 0.0))
        if self.__verticalDropdown:
            LayoutManager.addConnection((True, False), self._inner.getCore().getBody(), self.getBody(), (1.0, 1.0), (1.0, 1.0), keepSizeFix=False)
            LayoutManager.addConnection((False, True), self._inner.getCore().getBody(), self.getBody(), (0.0, 0.0), (1.0, 1.0))
        else:
            LayoutManager.addConnection((False, True), self._inner.getCore().getBody(), self.getBody(), (1.0, 1.0), (1.0, 1.0), keepSizeFix=False)
            LayoutManager.addConnection((True, False), self._inner.getCore().getBody(), self.getBody(), (0.0, 0.0), (1.0, 1.0))

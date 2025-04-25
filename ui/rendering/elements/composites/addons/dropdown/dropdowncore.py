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
        self._inner.alignpoint(self)
        if self.__verticalDropdown:
            self._inner.alignaxis(self, 1, keepSize=False)
            self._inner.alignnextto(self, 3)
        else:
            self._inner.alignaxis(self, 3, keepSize=False)
            self._inner.alignnextto(self, 1)

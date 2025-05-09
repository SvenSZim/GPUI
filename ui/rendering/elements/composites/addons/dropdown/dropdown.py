from typing import Any, override

from ......display      import Surface
from ......interaction  import InputManager, InputEvent,Clickable
from ....element        import Element
from ..addon            import Addon

from .dropdowncore         import DropdownCore
from .dropdowndata         import DropdownData
from .dropdowncreateoption import DropdownCO
from .dropdownprefab       import DropdownPrefab

class Dropdown(Addon[Element, DropdownCore, DropdownData, DropdownCO, DropdownPrefab], Clickable):

    # -------------------- creation --------------------

    def __init__(self, outer: Element, *inner: Element | tuple[Element, float], verticalDropdown: bool=True, dropdownActive: bool=True, offset: int=0,
                 renderData: DropdownPrefab | list[DropdownCO] | DropdownData=DropdownPrefab.BASIC, active: bool = True) -> None:
        assert self._renderstyle is not None

        if isinstance(renderData, list):
            myData: DropdownData = DropdownData()
            for createOption in renderData:
                myData += (createOption, self._renderstyle)
            renderData = myData
        elif isinstance(renderData, DropdownPrefab):
            renderData = DropdownData() * (renderData, self._renderstyle)

        Clickable.__init__(self, active)
        Addon.__init__(self, DropdownCore(outer, *inner, verticalDropdown=verticalDropdown, offset=offset, buttonActive=dropdownActive), renderData, active)
        
        self._core.addGlobalTriggerEvent(self._onclick)
        #Default trigger event: LEFTDOWN
        self.addTriggerEvent(InputManager.getEvent(InputEvent.LEFTDOWN))
    
    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'Dropdown':
        return Dropdown(args['outer'])

    # -------------------- rendering --------------------

    @override
    def render(self, surface: Surface) -> None:
        """
        render renders the UI-Element onto the given surface

        Args:
            surface (Surface): the surface the UIElement should be drawn on
        """
        assert self._drawer is not None

        if self._active:
            self._core.getOuter().render(surface)

            if self._core.getCurrentToggleState():
                self.addPostRenderElement(self._core.getInner())

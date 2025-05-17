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

    def __init__(self, outer: Element, *inner: Element | tuple[Element, float], verticalDropdown: bool=True, dropdownActive: bool=True, offset: int=0, active: bool = True) -> None:
        assert self._renderstyle is not None

        Clickable.__init__(self, active)
        Addon.__init__(self, DropdownCore(outer, *inner, verticalDropdown=verticalDropdown, offset=offset, buttonActive=dropdownActive), DropdownData(), active)
        
        self._core.addGlobalTriggerEvent(self._onclick)
        #Default trigger event: LEFTDOWN
        self.addTriggerEvent(InputManager.getEvent(InputEvent.LEFTDOWN))
    
    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'Dropdown':
        inner: list[Element] = args['inner']
        verticalDropdown = True
        offset = 0
        sizings: list[float] = [1.0 for _ in inner[1:]]
        for arg, v in args.items():
            match arg:
                case 'vertical' | 'vert':
                    verticalDropdown = True
                case 'horizontal' | 'hor':
                    verticalDropdown = False
                case 'offset' | 'spacing':
                    offset = int(Dropdown.extractNum(v))
                case 'size' | 'sizes' | 'sizing' | 'sizings':
                    sizings = list(map(Dropdown.parseNum, Dropdown.adjustList(list(map(str, sizings)), Dropdown.parseList(v))))
        return Dropdown(inner[0], *zip(inner[1:], sizings), verticalDropdown=verticalDropdown, offset=offset)

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
            self._core.getInner().render(surface)

            if self._core.getCurrentToggleState():
                self.addPostRenderElement(self._core.getDropdown())

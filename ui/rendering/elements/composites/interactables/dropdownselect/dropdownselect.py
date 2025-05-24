from typing import Any, Callable, override

from ......utility  import Rect
from ......display  import Surface
from ....element    import Element
from ..interactable import Interactable

from .dropdownselectcore         import DropdownselectCore
from .dropdownselectdata         import DropdownselectData

class Dropdownselect(Interactable[DropdownselectCore, DropdownselectData]):

    # -------------------- creation --------------------

    def __init__(self, rect: Rect, *inner: tuple[tuple[Element, float], Element], verticalDropdown: bool=True,
                 offset: int=0, startState: int=0, active: bool = True, args: dict[str, Any]={}) -> None:
        
        super().__init__(DropdownselectCore(rect, *inner, verticalDropdown=verticalDropdown, offset=offset, startState=startState, args=args), DropdownselectData(), active)
    
    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'Dropdownselect':
        inner: list[Element] = args['inner']
        verticalDropdown = True
        offset = 0
        sizings: list[float] = [1.0 for _ in inner[1::2]]
        for arg, v in args.items():
            match arg:
                case 'vertical' | 'vert':
                    verticalDropdown = True
                case 'horizontal' | 'hor':
                    verticalDropdown = False
                case 'offset' | 'spacing':
                    offset = int(Dropdownselect.extractNum(v))
                case 'size' | 'sizes' | 'sizing' | 'sizings':
                    sizings = list(map(Dropdownselect.parseNum, Dropdownselect.adjustList(list(map(str, sizings)), Dropdownselect.parseList(v))))
        return Dropdownselect(Rect(), *zip(zip(args['inner'][1::2], sizings), args['inner'][::2]), verticalDropdown=verticalDropdown, offset=offset, args=args)

    # -------------------- access-point --------------------

    @override
    def setActive(self, active: bool) -> None:
        super().setActive(active)
        self._core.setButtonActive(active)

    @override
    def toggleActive(self) -> bool:
        bb = super().toggleActive()
        self._core.setButtonActive(bb)
        return bb

    @override
    def set(self, args: dict[str, Any]) -> None:
        super().set(args)
        for tag, value in args.items():
            match tag:
                case 'subscribeToToggleState':
                    if isinstance(value, tuple) and isinstance(value[0], int) and isinstance(value[1], str):
                        self._core.subscribeToToggleState(value[0], value[1])
                    else:
                        raise ValueError('subscribeToSelect expects 2-tuple with the toggle state (int) and a callbackID')
                case 'unsubscribeToToggleState':
                    if isinstance(value, tuple) and isinstance(value[0], int) and isinstance(value[1], str):
                        self._core.unsubscribeToToggleState(value[0], value[1])
                    else:
                        raise ValueError('unsubscribeToToggleState expects 2-tuple with the toggle state (int) and a callbackID')
                case 'quickSubscribeToToggleState':
                    if isinstance(value, tuple) and isinstance(value[0], int) and isinstance(value[1], Callable) and isinstance(value[2], list):
                        self._core.quickSubscribeToToggleState(value[0], value[1], *value[2])
                    else:
                        raise ValueError('quickSubscribeToToggleState expects a 3-tuple the toggle state (int), with a Callable and a list of arguments')
    
    # -------------------- rendering --------------------

    @override
    def render(self, surface: Surface) -> None:
        """
        render renders the UI-Element onto the given surface

        Args:
            surface (Surface): the surface the UIElement should be drawn on
        """
        assert self._drawer is not None

        if self.isActive():
            self._core.getDropdown().render(surface)
            self._core.getOuter().render(surface)

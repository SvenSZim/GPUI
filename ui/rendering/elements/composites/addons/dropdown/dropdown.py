from typing import Any, Callable, override

from ......display      import Surface
from ......interaction  import InputManager, InputEvent, Clickable
from ....element        import Element
from ..addon            import Addon

from .dropdowncore         import DropdownCore
from .dropdowndata         import DropdownData

class Dropdown(Addon[DropdownCore, DropdownData], Clickable):

    # -------------------- creation --------------------

    def __init__(self, outer: Element, *inner: Element | tuple[Element, float], verticalDropdown: bool=True, dropdownActive: bool=True, offset: int=0, active: bool = True) -> None:
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

    # -------------------- access-point --------------------

    @override
    def set(self, args: dict[str, Any]) -> None:
        super().set(args)
        for tag, value in args.items():
            match tag:
                case 'setButtonActive':
                    if isinstance(value, bool):
                        self._core.setButtonActive(value)
                    else:
                        raise ValueError('setButtonActive expects a bool')
                case 'addTriggerEvent':
                    if isinstance(value, str):
                        self._core.addTriggerEvent(value)
                    else:
                        raise ValueError('addTriggerEvent expects a eventID')
                case 'removeTriggerEvent':
                    if isinstance(value, str):
                        self._core.removeTriggerEvent(value)
                    else:
                        raise ValueError('removeTriggerEvent expects a eventID')
                case 'addGlobalTriggerEvent':
                    if isinstance(value, str):
                        self._core.addGlobalTriggerEvent(value)
                    else:
                        raise ValueError('addGlobalTriggerEvent expects a eventID')
                case 'removeGlobalTriggerEvent':
                    if isinstance(value, str):
                        self._core.removeGlobalTriggerEvent(value)
                    else:
                        raise ValueError('removeGlobalTriggerEvent expects a eventID')
                case 'subscribeToClick':
                    if isinstance(value, str):
                        self._core.subscribeToClick(value)
                    else:
                        raise ValueError('subscribeToClick expects a callbackID')
                case 'unsubscribeToClick':
                    if isinstance(value, str):
                        self._core.unsubscribeToClick(value)
                    else:
                        raise ValueError('unsubscribeToClick expects a callbackID')
                case 'quickSubscribeToClick':
                    if isinstance(value, tuple) and isinstance(value[0], Callable) and isinstance(value[1], list):
                        self._core.quickSubscribeToClick(value[0], *value[1])
                    else:
                        raise ValueError('quickSubscribeToClick expects a 2-tuple with a Callable and a list of arguments')
                case 'subscribeToSelect':
                    if isinstance(value, str):
                        self._core.subscribeToToggleState(1, value)
                    else:
                        raise ValueError('subscribeToSelect expects a callbackID')
                case 'unsubscribeToSelect':
                    if isinstance(value, str):
                        self._core.unsubscribeToToggleState(1, value)
                    else:
                        raise ValueError('unsubscribeToSelect expects a callbackID')
                case 'quickSubscribeToSelect':
                    if isinstance(value, tuple) and isinstance(value[0], Callable) and isinstance(value[1], list):
                        self._core.quickSubscribeToToggleState(1, value[0], *value[1])
                    else:
                        raise ValueError('quickSubscribeToSelect expects a 2-tuple with a Callable and a list of arguments')
                case 'subscribeToDeselect':
                    if isinstance(value, str):
                        self._core.subscribeToToggleState(0, value)
                    else:
                        raise ValueError('subscribeToDeselect expects a callbackID')
                case 'unsubscribeToDeselect':
                    if isinstance(value, str):
                        self._core.unsubscribeToToggleState(0, value)
                    else:
                        raise ValueError('unsubscribeToDeselect expects a callbackID')
                case 'quickSubscribeToDeselect':
                    if isinstance(value, tuple) and isinstance(value[0], Callable) and isinstance(value[1], list):
                        self._core.quickSubscribeToToggleState(0, value[0], *value[1])
                    else:
                        raise ValueError('quickSubscribeToDeselect expects a 2-tuple with a Callable and a list of arguments')

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

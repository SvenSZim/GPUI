from typing import Any, Callable, Optional, override

from ......utility  import Rect
from ......display  import Surface
from ....element    import Element
from ..interactable import Interactable

from .multiselectcore         import MultiselectCore
from .multiselectdata         import MultiselectData

class Multiselect(Interactable[MultiselectCore, MultiselectData]):

    # -------------------- creation --------------------

    def __init__(self, rect: Rect, *inner: tuple[Element, float], alignVertical: bool=True, offset: int=0,
                 startState: int=0, restriction: Optional[Callable[[int], int]]=None, active: bool = True, args: dict[str, Any]={}) -> None:
        
        super().__init__(MultiselectCore(rect, *inner, alignVertical=alignVertical, offset=offset, startState=startState, restriction=restriction, args=args), MultiselectData(), active)
    
    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'Multiselect':
        inner: list[Element] = args['inner']
        alignVertical = True
        offset = 0
        sizings: list[float] = [1.0 for _ in inner]
        startState: int = 0
        limit: int = len(args['inner'])
        for arg, v in args.items():
            match arg.lower():
                case 'vertical' | 'vert':
                    alignVertical = True
                case 'horizontal' | 'hor':
                    alignVertical = False
                case 'offset' | 'spacing':
                    offset = int(Multiselect.extractNum(v))
                case 'size' | 'sizes' | 'sizing' | 'sizings':
                    sizings = list(map(Multiselect.parseNum, Multiselect.adjustList(list(map(str, sizings)), Multiselect.parseList(v))))
                
                case 'start' | 'startstate':
                    startState = int(Multiselect.extractNum(v))
                case 'max' | 'restr' | 'limit':
                    limit = int(Multiselect.extractNum(v))
        return Multiselect(Rect(), *zip(inner, sizings), alignVertical=alignVertical, offset=offset, startState=startState,
                           restriction=lambda x, m=len(args['inner']), l=limit: 2**m-1 if bin(x)[2:].count('1') < l else x, args=args)

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
                case 'subscribeToSelectorSelect':
                    if isinstance(value, tuple) and isinstance(value[0], int) and isinstance(value[1], str):
                        self._core.subscribeToSelectorSelect(value[0], value[1])
                    else:
                        raise ValueError('subscribeToSelectorSelect expects 2-tuple with the toggle state (int) and a callbackID')
                case 'unsubscribeToSelectorSelect':
                    if isinstance(value, tuple) and isinstance(value[0], int) and isinstance(value[1], str):
                        self._core.unsubscribeToSelectorSelect(value[0], value[1])
                    else:
                        raise ValueError('unsubscribeToSelectorSelect expects 2-tuple with the toggle state (int) and a callbackID')
                case 'quickSubscribeToSelectorSelect':
                    if isinstance(value, tuple) and isinstance(value[0], int) and isinstance(value[1], Callable) and isinstance(value[2], list):
                        self._core.quicksubscribeToSelectorSelect(value[0], value[1], *value[2])
                    else:
                        raise ValueError('quickSubscribeToSelectorSelect expects a 3-tuple the toggle state (int), with a Callable and a list of arguments')
                case 'subscribeToSelectorSelect':
                    if isinstance(value, tuple) and isinstance(value[0], int) and isinstance(value[1], str):
                        self._core.subscribeToSelectorDeselect(value[0], value[1])
                    else:
                        raise ValueError('subscribeToSelectorDeselect expects 2-tuple with the toggle state (int) and a callbackID')
                case 'unsubscribeToSelectorDeselect':
                    if isinstance(value, tuple) and isinstance(value[0], int) and isinstance(value[1], str):
                        self._core.unsubscribeToSelectorDeselect(value[0], value[1])
                    else:
                        raise ValueError('unsubscribeToSelectorDeselect expects 2-tuple with the toggle state (int) and a callbackID')
                case 'quickSubscribeToSelectorDeselect':
                    if isinstance(value, tuple) and isinstance(value[0], int) and isinstance(value[1], Callable) and isinstance(value[2], list):
                        self._core.quicksubscribeToSelectorDeselect(value[0], value[1], *value[2])
                    else:
                        raise ValueError('quickSubscribeToSelectorDeselect expects a 3-tuple the toggle state (int), with a Callable and a list of arguments')

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
            self._core.getInner().render(surface)

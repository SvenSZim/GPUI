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
    def set(self, args: dict[str, Any], sets: int = -1, maxDepth: int = -1) -> int:
        """
        set is a general access point to an element. It has some basic functionality implemented and is overridden
        by some elements for more specific behavior (updating text in Text, subscribing to buttonpresses in button, etc.).
        set also recursivly applies the given args to all children until the given amount of
        'sets' or the maxDepth is reached. A 'set' is counted, if any of the given args can be applied to the element.

        Returns (int): the amount of 'sets' applied
        """
        return super().set(args, sets, maxDepth)
        for tag, value in args.items():
            match tag:
                case _:
                    pass

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

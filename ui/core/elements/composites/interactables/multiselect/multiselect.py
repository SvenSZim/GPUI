from typing import Any, override

from ......display  import Surface
from ....element    import Element
from ...addons      import Grouped
from ..interactable import Interactable

from .multiselectcore         import MultiselectCore
from .multiselectdata         import MultiselectData

class Multiselect(Interactable[MultiselectCore, MultiselectData]):

    # -------------------- creation --------------------

    def __init__(self, core: MultiselectCore, renderData: MultiselectData, active: bool = True) -> None:
        super().__init__(core, renderData, active)
        renderData.alignInner(self)
    
    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'Multiselect':
        inner: list[Element] = args['inner']
        gpdargs: dict[str, Any] = {}
        startState: int = 0
        limit: int = len(args['inner'])
        for arg, v in args.items():
            match arg.lower():
                case 'vertical' | 'vert':
                    gpdargs['vert'] = v
                case 'horizontal' | 'hor':
                    gpdargs['hor'] = v
                case 'offset' | 'spacing':
                    gpdargs['offset'] = v
                case 'size' | 'sizes' | 'sizing' | 'sizings':
                    gpdargs['size'] = v

                case 'start' | 'startstate':
                    startState = int(Multiselect.extractNum(v))
                case 'max' | 'restr' | 'limit':
                    limit = int(Multiselect.extractNum(v))
        gpdargs['inner'] = inner
        data = MultiselectData(Grouped.parseFromArgs(gpdargs))
        core = MultiselectCore(inner, startState=startState, restriction=lambda x, m=len(args['inner']), l=limit: 2**m-1 if bin(x)[2:].count('1') < l else x)
        return Multiselect(core, data)

    @override
    def getInnerSizing(self, elSize: tuple[int, int], args: dict[str, Any]={}) -> tuple[int, int]:
        return self._renderData.group.getInnerSizing(elSize, args)

    # -------------------- access-point --------------------

    @override
    def set(self, args: dict[str, Any], sets: int = -1, maxDepth: int = -1, skips: list[int] = [0]) -> int:
        """
        set is a general access point to an element. It has some basic functionality implemented and is overridden
        by some elements for more specific behavior (updating text in Text, subscribing to buttonpresses in button, etc.).
        set also recursivly applies the given args to all children until the given amount of
        'sets' or the maxDepth is reached. A 'set' is counted, if any of the given args can be applied to the element.

        Returns (int): the amount of 'sets' applied
        """
        ts: int = 0
        s: bool = self._set(args, sets, maxDepth, bool(skips[0]))
        ts += int(s and not skips[0])
        if 0 <= maxDepth < 2:
            return ts
        skips[0] = max(0, skips[0]-ts)
        if sets < 0 or ts < sets:
            cs: int = self._renderData.setinner(args, sets-ts, maxDepth-1, skips)
            skips[0] = max(0, skips[0]-cs)
            ts += cs
        return ts

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
            self._renderData.group.render(surface)

from typing import Any, override

from ......display   import Surface
from ....element     import Element
from ..addon         import Addon

from .groupedcore         import GroupedCore
from .groupeddata         import GroupedData

class Grouped(Addon[GroupedCore, GroupedData]):
    """An addon that arranges multiple elements in a vertical or horizontal group.
    
    Provides layout organization features including:
    - Vertical or horizontal arrangement of elements
    - Configurable spacing between elements
    - Relative sizing through element weights
    - Automatic alignment and distribution
    
    Used for creating structured layouts like toolbars, sidebars,
    or any interface component requiring organized arrangement of
    multiple elements with controlled spacing and sizing.
    """

    # -------------------- creation --------------------

    def __init__(self, inner: list[tuple[Element, float]], alignVertical: bool=True, offset: int=0, active: bool = True) -> None:
        super().__init__(GroupedCore(inner, alignVertical=alignVertical, offset=offset), GroupedData(), active)

    @staticmethod
    @override
    def getMinRequiredChildren() -> int:
        return 1

    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'Grouped':
        inner: list[Element] = args['inner']
        alignVertical = True
        offset = 0
        sizings: list[float] = [1.0 for _ in inner]
        for arg, v in args.items():
            match arg:
                case 'vertical' | 'vert':
                    alignVertical = True
                case 'horizontal' | 'hor':
                    alignVertical = False
                case 'offset' | 'spacing':
                    offset = int(Grouped.extractNum(v))
                case 'size' | 'sizes' | 'sizing' | 'sizings':
                    sizings = list(map(Grouped.parseNum, Grouped.adjustList(list(map(str, sizings)), Grouped.parseList(v))))
        return Grouped(list(zip(inner, sizings)), alignVertical=alignVertical, offset=offset)

    #-------------------- access-point --------------------

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
            cs: int = self._core.setinner(args, sets-ts, maxDepth-1, skips)
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
            for el in self._core.getInner():
                el.render(surface)

from typing import Any, override

from ......utility   import Rect
from ......display   import Surface
from ....element     import Element
from ..addon         import Addon

from .groupedcore         import GroupedCore
from .groupeddata         import GroupedData

class Grouped(Addon[GroupedCore, GroupedData]):

    # -------------------- creation --------------------

    def __init__(self, rect: Rect, *inner: Element | tuple[Element, float], alignVertical: bool=True, offset: int=0, active: bool = True) -> None:
        super().__init__(GroupedCore(rect, *inner, alignVertical=alignVertical, offset=offset), GroupedData(), active)
    
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
        return Grouped(Rect(), *zip(inner, sizings), alignVertical=alignVertical, offset=offset)

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
            for el in self._core.getInner():
                el.render(surface)

from typing import Any, override

from ......display   import Surface
from ....element     import Element
from ....atoms       import Box, Line
from ..addon         import Addon

from .framedcore         import FramedCore
from .frameddata         import FramedData

class Framed(Addon[FramedCore, FramedData]):
    
    # -------------------- creation --------------------

    def __init__(self, inner: Element, renderData: FramedData, offset: int=0, active: bool = True) -> None:
        super().__init__(FramedCore(inner, offset=offset), renderData, active)
        self._renderData.alignInner(self)

    def getArgs(self) -> dict[str, Any]:
        return {'inner':[x.copy() for x in self._renderData.borderData] + [self._renderData.fillData.copy()], 'inset':str(self._core.getOffset())}
    
    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'Framed':
        inner: list[Element] = args['inner']
        if not len(inner):
            raise ValueError("Insufficient amount of children in Framed!")

        offset: int = 0
        for arg, v in args.items():
            match arg:
                case 'offset' | 'padding' | 'inset':
                    offset = int(Framed.extractNum(v))
        
        types = [0 if isinstance(x, Line) else 1 if isinstance(x, Box) else 2 for x in inner]
        if len(inner) == 1:
            return Framed(inner[0], FramedData.parseFromArgs(args), offset=offset)
        elif 2 in types:
            return Framed(inner[types.index(2)], FramedData.parseFromArgs(args), offset=offset)
        elif types.count(1) > 1:
            return Framed(inner[1-types.index(1)], FramedData.parseFromArgs(args), offset=offset)
        elif 1 in types:
            return Framed(inner[types.index(1)], FramedData.parseFromArgs(args), offset=offset)
        else:
            raise ValueError("No frameable children in Framed!")

    # -------------------- rendering --------------------

    @override
    def render(self, surface: Surface) -> None:
        """
        render renders the UI-Element onto the given surface

        Args:
            surface (Surface): the surface the UIElement should be drawn on
        """
        assert self._drawer is not None
        
        # background
        self._renderData.fillData.render(surface)

        # inner element
        self._core.getInner().render(surface)

        # outlines
        for border in self._renderData.borderData:
            border.render(surface)

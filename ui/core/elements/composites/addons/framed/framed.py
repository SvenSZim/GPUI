from typing import Any, override

from ......display   import Surface
from ....element     import Element
from ....atoms       import Box, Line
from ..addon         import Addon

from .framedcore         import FramedCore
from .frameddata         import FramedData

class Framed(Addon[FramedCore, FramedData]):

    # -------------------- creation --------------------

    def __init__(self, inner: Element, renderData: FramedData | dict[str, Any], offset: int=0, active: bool = True) -> None:
        if isinstance(renderData, dict):
            renderData = FramedData.parseFromArgs(renderData)
        super().__init__(FramedCore(inner, offset=offset), renderData, active)
        self._renderData.alignInner(self)

    def getArgs(self) -> dict[str, Any]:
        return {'inner':[x.copy() for x in self._renderData.borderData] + [self._renderData.fillData.copy()], 'inset':str(self._core.getOffset())}

    @staticmethod
    @override
    def getMinRequiredChildren() -> int:
        return 1

    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'Framed':
        inner: list[Element] = args['inner']

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

    #-------------------- access-point --------------------

    def set(self, args: dict[str, Any], sets: int=-1, maxDepth: int=-1) -> int:
        """
        set is a general access point to an element. It has some basic functionality implemented and is overridden
        by some elements for more specific behavior (updating text in Text, subscribing to buttonpresses in button, etc.).
        set also recursivly applies the given args to all children until the given amount of
        'sets' or the maxDepth is reached. A 'set' is counted, if any of the given args can be applied to the element.

        Returns (int): the amount of 'sets' applied
        """
        s: int = super().set(args, sets, maxDepth)
        if 0 <= maxDepth < 2:
            return s
        if sets < 0 or s < sets:
            s += self._renderData.setinner(args, sets-s, maxDepth-1)
        if sets < 0 or s < sets:
            s += self._core.setinner(args, sets-s, maxDepth-1)
        return s

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
            # background
            self._renderData.fillData.render(surface)

            # inner element
            self._core.getInner().render(surface)

            # outlines
            for border in self._renderData.borderData:
                border.render(surface)

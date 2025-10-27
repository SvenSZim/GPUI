from typing import Any, Optional, override

from ......utility   import StyledDefault
from ......display   import Surface
from ....element     import Element
from ....atoms       import Box, Line
from ..addon         import Addon

from .framedcore         import FramedCore
from .frameddata         import FramedData

class Framed(Addon[FramedCore, FramedData]):
    """An addon that adds a customizable frame around an element.
    
    Enhances elements with visual framing features including:
    - Configurable border elements on all sides
    - Optional background element
    - Adjustable padding/offset from content
    - Support for styled borders and backgrounds
    
    Commonly used to add visual structure through borders, backgrounds,
    and spacing around content elements. Supports both uniform and
    individually styled borders for flexible visual design.
    """

    # -------------------- creation --------------------

    def __init__(self, inner: Element, renderData: FramedData, offset: int=0, active: bool = True) -> None:
        super().__init__(FramedCore(inner, offset=offset), renderData, active)
        self._renderData.alignInner(self)

    @staticmethod
    @override
    def getMinRequiredChildren() -> int:
        return 1

    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'Framed':
        inner: list[Element] = args['inner']
        style: str = args['fixstyle']

        offset: int = 0
        str_bg: str = str(StyledDefault.BACKGROUND)
        str_border: str = str(StyledDefault.BORDER)
        for arg, v in args.items():
            match arg:
                case 'offset' | 'padding' | 'inset':
                    offset = int(Framed.extractNum(v))
                case 'bg' | 'background':
                    str_bg = v.strip()
                case 'border':
                    str_border = v.strip()
        
        pbg: Optional[Element] = Framed.getStyledElement(str_bg, style)
        pborders: tuple[Optional[Element], Optional[Element], Optional[Element], Optional[Element]] =\
                 (Framed.getStyledElement(str_border, style), Framed.getStyledElement(str_border, style),
                  Framed.getStyledElement(str_border, style), Framed.getStyledElement(str_border, style))
        bg: Element = Box.parseFromArgs({}) if pbg is None else pbg
        borders: tuple[Element, Element, Element, Element] =\
                (Line.parseFromArgs({}) if pborders[0] is None else pborders[0],
                 Line.parseFromArgs({}) if pborders[1] is None else pborders[1],
                 Line.parseFromArgs({}) if pborders[2] is None else pborders[2],
                 Line.parseFromArgs({}) if pborders[3] is None else pborders[3])

        if len(inner) == 1:
            return Framed(inner[0], FramedData(bg, borders), offset=offset)
        else:
            types = [0 if isinstance(x, Line) else 1 if isinstance(x, Box) else 2 for x in inner]
            if 0 in types:
                if types.count(0) > 1:
                    bds = list(borders)
                    b = 0
                    for i, k in enumerate(types):
                        if k == 0:
                            bds[b] = inner[i]
                            b += 1
                            if b > 3:
                                break
                    borders = (bds[0], bds[1], bds[2], bds[3])
                else:
                    b = inner[types.index(0)]
                    assert isinstance(b, Line)
                    borders = (b, b.copy(), b.copy(), b.copy())
            if 2 in types:
                if 1 in types:
                    bg = inner[types.index(1)]
                return Framed(inner[types.index(2)], FramedData(bg, borders), offset=offset)
            elif types.count(1) > 1:
                return Framed(inner[types.index(1, types.index(1)+1)], FramedData(inner[types.index(1)], borders), offset=offset)
            elif 1 in types:
                return Framed(inner[types.index(1)], FramedData(bg, borders), offset=offset)
            else:
                raise ValueError("No frameable children in Framed!")

    #-------------------- access-point --------------------

    @override
    def _set(self, args: dict[str, Any], sets: int = -1, maxDepth: int = -1, skips: bool = False) -> bool:
        return super()._set(args, sets, maxDepth, skips)

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
            # background
            self._renderData.fillData.render(surface)

            # inner element
            self._core.getInner().render(surface)

            # outlines
            for border in self._renderData.borderData:
                border.render(surface)

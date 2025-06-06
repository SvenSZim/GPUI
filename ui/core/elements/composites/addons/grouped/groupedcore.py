from typing import Any, override

from ......utility import Rect
from ....element   import Element
from ....atoms     import Box
from ..addoncore   import AddonCore

class GroupedCore(AddonCore[list[Element]]):
    """
    GroupedCore is the core object of the addon 'Grouped'.
    """
    __alignVertical: bool
    __offset: int
    __relativeSizing: list[float]

    def __init__(self, inner: list[tuple[Element, float]], alignVertical: bool=True, offset: int=0) -> None:
        self.__alignVertical = alignVertical
        self.__offset = offset

        self.__relativeSizing = [el[1] for el in inner]

        super().__init__(Rect(), [el[0] for el in inner])

    @override
    def _alignInner(self) -> None:
        if len(self._inner) == 0:
            return

        virtualBox = Box.parseFromArgs({})
        totalSize: float = sum(self.__relativeSizing)
        if totalSize == 0.0:
            totalSize = 1.0

        if self.__alignVertical:
            virtualBox.align(self, offset=(0, -int(0.5*self.__offset)))
            virtualBox.alignSize(self, absoluteOffset=(0, self.__offset))

            relHeight: float = 0.0
            for nr, el in enumerate(self._inner):
                el.alignpoint(virtualBox, otherPoint=(0,relHeight/totalSize), offset=(0,int(0.5*self.__offset)))
                relHeight += self.__relativeSizing[nr]
                el.alignSize(virtualBox, relativeAlign=(1, self.__relativeSizing[nr]/totalSize), absoluteOffset=(0, -self.__offset))
        else:
            virtualBox.align(self, offset=(-int(0.5*self.__offset),0))
            virtualBox.alignSize(self, absoluteOffset=(self.__offset, 0))

            relWidth: float = 0.0
            for nr, el in enumerate(self._inner):
                el.alignpoint(virtualBox, otherPoint=(relWidth/totalSize,0), offset=(int(0.5*self.__offset),0))
                relWidth += self.__relativeSizing[nr]
                el.alignSize(virtualBox, relativeAlign=(self.__relativeSizing[nr]/totalSize, 1), absoluteOffset=(-self.__offset, 0))

    @override
    def getInnerSizing(self, elSize: tuple[int, int], args: dict[str, Any]) -> tuple[int, int]:
        if self.__alignVertical:
            maxWidth, totHeight = 0, -self.__offset if args.get('relative', False) else 0
            for el, relSizY in zip(self._inner, self.__relativeSizing):
                x, y = el.getInnerSizing(elSize, args)
                if x > maxWidth:
                    maxWidth = x
                totHeight += int(relSizY * y) + (self.__offset if args.get('relative', False) else 0)
            return maxWidth, max(0, totHeight)
        else:
            totWidth, maxHeight = -self.__offset if args.get('relative', False) else 0, 0
            for el, relSizX in zip(self._inner, self.__relativeSizing):
                x, y = el.getInnerSizing(elSize, args)
                totWidth += int(relSizX * x) + (self.__offset if args.get('relative', False) else 0)
                if y > maxHeight:
                    maxHeight = y
            return max(0, totWidth), maxHeight

    @override
    def setActive(self, active: bool) -> None:
        for el in self._inner:
            el.setActive(active)

    # -------------------- access-point --------------------

    def setinner(self, args: dict[str, Any], sets: int=-1, maxDepth: int=-1, skips: list[int]=[0]) -> int:
        s: int = 0
        cs: int
        for el in self._inner:
            if sets < 0 or s < sets:
                cs = el.set(args, sets-s, maxDepth, skips)
                skips[0] = max(0, skips[0]-cs)
                s += cs
        return s

from typing import Any, override

from ......utility import Rect, AlignType
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

    def __init__(self, rect: Rect, *inner: Element | tuple[Element, float], alignVertical: bool=True, offset: int=0) -> None:
        self.__alignVertical = alignVertical
        self.__offset = offset

        self.__relativeSizing = [0.0 for _ in range(len(inner))]
        if len(inner) > 0:
            cSum: float = sum([0 if isinstance(x, Element) else abs(x[1]) for x in inner])
            notSized: int = sum([1 if isinstance(x, Element) else 0 for x in inner])
            if cSum >= 1.0 or not notSized:
                for i, x in enumerate(inner):
                    if isinstance(x, tuple):
                        self.__relativeSizing[i] = abs(x[1]) / cSum
            else:
                for i, x in enumerate(inner):
                    if isinstance(x, tuple):
                        self.__relativeSizing[i] = abs(x[1])
                    else:
                        self.__relativeSizing[i] = (1.0 - cSum) / notSized

        super().__init__(rect, [el if isinstance(el, Element) else el[0] for el in inner])
    
    @override
    def _alignInner(self) -> None:
        if len(self._inner) == 0:
            return

        virtualBox = Box.parseFromArgs({})
        
        if self.__alignVertical:
            virtualBox.align(self, offset=(0, -int(0.5*self.__offset)))
            virtualBox.align(self, align=AlignType.iBiR, offset=(0, int(0.5*self.__offset)), keepSize=False)
                                  
            usedHeightPercent: float = 0.0

            for nr, el in enumerate(self._inner):
                el.alignpoint(virtualBox, otherPoint=(0,usedHeightPercent), offset=(0,int(0.5*self.__offset)))
                usedHeightPercent += self.__relativeSizing[nr]
                el.alignpoint(virtualBox, (1,1), (1,usedHeightPercent), offset=(0,-int(0.5*self.__offset)), keepSize=False)

        else:
            virtualBox.align(self, offset=(-int(0.5*self.__offset),0))
            virtualBox.align(self, align=AlignType.iBiR, offset=(int(0.5*self.__offset),0), keepSize=False)

            usedWidthPercent: float = 0.0

            for nr, el in enumerate(self._inner):
                el.alignpoint(virtualBox, otherPoint=(usedWidthPercent,0), offset=(int(0.5*self.__offset),0))
                usedWidthPercent += self.__relativeSizing[nr]
                el.alignpoint(virtualBox, (1,1), (usedWidthPercent,1), offset=(-int(0.5*self.__offset),0), keepSize=False)

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

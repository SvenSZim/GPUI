from typing import Any, override

from ......utility import Rect
from ....element   import Element
from ..addoncore   import AddonCore

class FramedCore(AddonCore[Element]):
    """
    FramedCore is the core object of the addon 'Framed'.
    """
    __offset: int

    # -------------------- creation --------------------

    def __init__(self, inner: Element, offset: int=0) -> None:
        self.__offset = offset
        rect: Rect = Rect((inner.getLeft() - self.__offset, inner.getTop() - self.__offset), (inner.getWidth() + 2 * self.__offset, inner.getHeight() + 2 * self.__offset))
        super().__init__(rect, inner)

    # -------------------- inner --------------------

    @override
    def _alignInner(self) -> None:
        self._inner.align(self, offset=self.__offset)
        self._inner.alignSize(self, absoluteOffset=-2 * self.__offset)

    def getOffset(self) -> int:
        return self.__offset

    @override
    def getInnerSizing(self, elSize: tuple[int, int], args: dict[str, Any]) -> tuple[int, int]:
        x, y = self._inner.getInnerSizing(elSize, args)
        if 'relative' in args:
            return x, y
        return x + self.__offset, y + self.__offset

    def setinner(self, args: dict[str, Any], sets: int=-1, maxDepth: int=-1, skips: list[int]=[0]) -> int:
        return self._inner.set(args, sets, maxDepth, skips)
    
    @override
    def setZIndex(self, zindex: int) -> None:
        self._inner.setZIndex(zindex)

    # -------------------- active-state --------------------

    @override
    def setActive(self, active: bool) -> None:
        self._inner.setActive(active)


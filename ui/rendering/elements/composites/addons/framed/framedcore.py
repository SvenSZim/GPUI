
from typing import override
from ......utility import Rect
from ....body      import LayoutManager
from ....element   import Element
from ..addoncore   import AddonCore

class FramedCore(AddonCore[Element]):
    """
    FramedCore is the core object of the addon 'Framed'.
    """
    __offset: int

    def __init__(self, inner: Element, offset: int=0) -> None:
        self.__offset = offset
        rect: Rect = Rect((inner.getLeft() - self.__offset, inner.getTop() - self.__offset), (inner.getWidth() + 2 * self.__offset, inner.getHeight() + 2 * self.__offset))
        super().__init__(rect, inner)

    @override
    def _alignInner(self) -> None:
        LayoutManager.addConnection((True, True), self._inner.getCore().getBody(), self.getBody(), (0.0, 0.0), (0.0, 0.0), self.__offset)
        LayoutManager.addConnection((True, True), self._inner.getCore().getBody(), self.getBody(), (1.0, 1.0), (1.0, 1.0), -self.__offset, keepSizeFix=False)

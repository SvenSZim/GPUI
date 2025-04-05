
from typing import override
from ......utility import Rect
from ....body      import LayoutManager
from ....element   import Element
from ..addoncore   import AddonCore

class GroupedCore(AddonCore[list[Element]]):
    """
    GroupedCore is the core object of the addon 'Grouped'.
    """
    __alignVertical: bool
    __offset: int

    def __init__(self, rect: Rect, *inner: Element, alignVertical: bool=True, offset: int=0) -> None:
        self.__alignVertical = alignVertical
        self.__offset = offset
        super().__init__(rect, list(inner))
        print(self.getInner())

    @override
    def _scaleUpdate(self, rect: Rect) -> None:
        self.__preAlign(rect)

    def __preAlign(self, rect: Rect) -> None:
        if len(self._inner) == 0:
            return
        
        LayoutManager.addConnection((True, True), self._inner[0].getCore().getBody(), self.getBody(), (0.0, 0.0), (0.0, 0.0))
        
        if self.__alignVertical:
            elementHeight: int = int((rect.height - self.__offset * (len(self._inner) - 1)) / len(self._inner))
            LayoutManager.addConnection((True, True), self._inner[0].getCore().getBody(), Rect(topleft=(rect.width, elementHeight)),
                                        (1.0, 1.0), (0.0, 0.0), keepSizeFix=False, fixedGlobal=False)
            for nr, el in enumerate(self._inner):
                if nr == 0:
                    continue
                LayoutManager.addConnection((True, True), el.getCore().getBody(), self._inner[nr-1].getCore().getBody(), (0.0, 0.0), (0.0, 1.0), (0, self.__offset))
                LayoutManager.addConnection((True, True), el.getCore().getBody(), Rect(topleft=(rect.width, elementHeight)),
                                            (1.0, 1.0), (0.0, 0.0), keepSizeFix=False, fixedGlobal=False)
        else:
            elementWidth: int = int((rect.width - self.__offset * (len(self._inner) - 1)) / len(self._inner))
            LayoutManager.addConnection((True, True), self._inner[0].getCore().getBody(), Rect(topleft=(elementWidth, rect.height)),
                                        (1.0, 1.0), (0.0, 0.0), keepSizeFix=False, fixedGlobal=False)
            for nr, el in enumerate(self._inner):
                if nr == 0:
                    continue
                LayoutManager.addConnection((True, True), el.getCore().getBody(), self._inner[nr-1].getCore().getBody(), (0.0, 0.0), (1.0, 0.0), (self.__offset, 0))
                LayoutManager.addConnection((True, True), el.getCore().getBody(), Rect(topleft=(elementWidth, rect.height)),
                                            (1.0, 1.0), (0.0, 0.0), keepSizeFix=False, fixedGlobal=False)

    @override
    def _alignInner(self) -> None:
        self.__preAlign(self.getRect())

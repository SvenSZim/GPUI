
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
    __relativeSizing: list[float]

    def __init__(self, rect: Rect, *inner: Element | tuple[Element, float], alignVertical: bool=True, offset: int=0) -> None:
        self.__alignVertical = alignVertical
        self.__offset = offset

        self.__relativeSizing = [0.0 for _ in range(len(inner))]
        if len(inner) > 0:
            cSum: float = sum([0 if isinstance(x, Element) else abs(x[1]) for x in inner])
            notSized: int = sum([1 if isinstance(x, Element) else 0 for x in inner])
            if cSum >= 1.0 or notSized == 0:
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
        
        LayoutManager.addConnection((True, True), self._inner[0].getCore().getBody(), self.getBody(), (0.0, 0.0), (0.0, 0.0))
        
        if self.__alignVertical:
            LayoutManager.addConnection((True, False), self._inner[0].getCore().getBody(), self.getBody(),
                                        (1.0, 0.0), (1.0, 0.0), keepSizeFix=False)
            availableHeight: float = self.getHeight() - self.__offset * (len(self._inner) - 1)
            usedHeightPercent: float = (availableHeight * self.__relativeSizing[0]) / self.getHeight()
            LayoutManager.addConnection((False, True), self._inner[0].getCore().getBody(), self.getBody(),
                                        (0.0, 1.0), (0.0, usedHeightPercent), keepSizeFix=False)
            for nr, el in enumerate(self._inner):
                if nr == 0:
                    continue
                LayoutManager.addConnection((True, True), el.getCore().getBody(), self._inner[nr-1].getCore().getBody(), (0.0, 0.0), (0.0, 1.0), (0, self.__offset))
                LayoutManager.addConnection((True, False), el.getCore().getBody(), self.getBody(),
                                            (1.0, 0.0), (1.0, 0.0), keepSizeFix=False)
                usedHeightPercent += self.__offset / self.getHeight()
                usedHeightPercent += (availableHeight * self.__relativeSizing[nr]) / self.getHeight()
                LayoutManager.addConnection((False, True), el.getCore().getBody(), self.getBody(),
                                            (0.0, 1.0), (0.0, usedHeightPercent), keepSizeFix=False)
        else:
            availableWidth: float = self.getWidth() - self.__offset * (len(self._inner) - 1)
            usedWidthPercent: float = (availableWidth * self.__relativeSizing[0]) / self.getWidth()
            LayoutManager.addConnection((True, False), self._inner[0].getCore().getBody(), self.getBody(),
                                        (1.0, 0.0), (usedWidthPercent, 0.0), keepSizeFix=False)
            LayoutManager.addConnection((False, True), self._inner[0].getCore().getBody(), self.getBody(),
                                        (0.0, 1.0), (0.0, 1.0), keepSizeFix=False)
            for nr, el in enumerate(self._inner):
                if nr == 0:
                    continue
                LayoutManager.addConnection((True, True), el.getCore().getBody(), self._inner[nr-1].getCore().getBody(), (0.0, 0.0), (1.0, 0.0), (self.__offset, 0))
                usedWidthPercent += self.__offset / self.getWidth()
                usedWidthPercent += (availableWidth * self.__relativeSizing[nr]) / self.getWidth()
                LayoutManager.addConnection((True, False), el.getCore().getBody(), self.getBody(),
                                            (1.0, 0.0), (usedWidthPercent, 0.0), keepSizeFix=False)
                LayoutManager.addConnection((False, True), el.getCore().getBody(), self.getBody(),
                                            (0.0, 1.0), (0.0, 1.0), keepSizeFix=False)

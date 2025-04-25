from typing import override

from ......utility import Rect
from ....body      import LayoutManager
from ....element   import Element
from ..addoncore   import AddonCore

class StackCore(AddonCore[list[Element]]):
    """
    StackCore is the core object of the addon 'Stack'.
    """
    __elementSizing: tuple[int, int]
    __alignVertical: bool
    __offset: int
    __relativeSizing: list[float]

    def __init__(self, rect: Rect, elementSizing: Rect, *inner: Element | tuple[Element, float], alignVertical: bool=True, offset: int=0) -> None:
        self.__elementSizing = elementSizing.getSize()
        self.__alignVertical = alignVertical
        self.__offset = offset

        self.__relativeSizing = [1.0 if isinstance(el, Element) else el[1] for el in inner]

        preRect: Rect
        if alignVertical:
            preRect = Rect(rect.getPosition(),
                           (elementSizing.getWidth(),
                            int(elementSizing.getHeight() * sum(self.__relativeSizing)) + offset * (len(self.__relativeSizing) - 1))
                          )
        else:
            preRect = Rect(rect.getPosition(),
                           (int(elementSizing.getWidth() * sum(self.__relativeSizing)) + offset * (len(self.__relativeSizing) - 1),
                            elementSizing.getHeight())
                          )

        super().__init__(preRect, [el if isinstance(el, Element) else el[0] for el in inner])
    
    @override
    def _alignInner(self) -> None:
        if len(self._inner) == 0:
            return

        if self.__alignVertical:
            totalHeight: float = 0.0
            for nr, (el, relSiz) in enumerate(zip(self._inner, self.__relativeSizing)):
                if nr > 0:
                    totalHeight = round(totalHeight + self.__offset / self.getHeight(), 2)
                el.alignpoint(self, otherPoint=(0,totalHeight))
                totalHeight = round(totalHeight + self.__elementSizing[1] * relSiz / self.getHeight(), 2)
                el.alignpoint(self, (1,1), (1,totalHeight), keepSize=False)
            self._inner[-1].alignpoint(self, (1,1), (1,1), keepSize=False)
        else:
            totalWidth: float = 0.0
            for nr, (el, relSiz) in enumerate(zip(self._inner, self.__relativeSizing)):
                if nr > 0:
                    totalWidth = round(totalWidth + self.__offset / self.getWidth(), 2)
                el.alignpoint(self, otherPoint=(totalWidth,0))
                totalWidth = round(totalWidth + self.__elementSizing[0] * relSiz / self.getWidth(), 2)
                el.alignpoint(self, (1,1), (totalWidth,1), keepSize=False)
            self._inner[-1].alignpoint(self, (1,1), (1,1), keepSize=False)

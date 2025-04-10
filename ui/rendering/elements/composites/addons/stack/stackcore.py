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

        super().__init__(rect, [el if isinstance(el, Element) else el[0] for el in inner])
    
    @override
    def _alignInner(self) -> None:
        if len(self._inner) == 0:
            return

        if self.__alignVertical:
            LayoutManager.addConnection((True, False), self.getBody(), Rect(), (1.0, 0.0), (0.0, 0.0), offset=self.__elementSizing[0], fixedGlobal=False, keepSizeFix=False)
            totalHeight: int = 0
            for idx, (el, relSiz) in enumerate(zip(self._inner, self.__relativeSizing)):
                # set sizes of elements
                LayoutManager.addConnection((True, False), el.getCore().getBody(), self.getBody(), (0.5, 0.0), (0.5, 0.0))
                LayoutManager.addConnection((True, False), el.getCore().getBody(), Rect(), (1.0, 0.0), (1.0, 0.0),
                                            offset=self.__elementSizing[0], fixedGlobal=False, keepSizeFix=False)
                height: int = int(self.__elementSizing[1] * relSiz)
                LayoutManager.addConnection((False, True), el.getCore().getBody(), Rect(), (0.0, 1.0), (0.0, 1.0),
                                            offset=height, fixedGlobal=False, keepSizeFix=False)
                # align elements below each other
                if idx == 0:
                    LayoutManager.addConnection((False, True), el.getCore().getBody(), self.getBody(), (0.0, 0.0), (0.0, 0.0))
                    totalHeight += height
                else:
                    LayoutManager.addConnection((False, True), el.getCore().getBody(), self._inner[idx-1].getCore().getBody(),
                                                (0.0, 0.0), (0.0, 1.0), offset=self.__offset)
                    totalHeight += height + self.__offset
            LayoutManager.addConnection((False, True), self.getBody(), Rect(), (0.0, 1.0), (0.0, 1.0), offset=totalHeight, fixedGlobal=False, keepSizeFix=False)
            #LayoutManager.addConnection((False, True), self.getBody(), self._inner[-1].getCore().getBody(),
            #                            (0.0, 1.0), (0.0, 1.0), keepSizeFix=False)
        else:
            totalWidth: int = 0
            for idx, (el, relSiz) in enumerate(zip(self._inner, self.__relativeSizing)):
                # set sizes of elements
                width: int = int(self.__elementSizing[0] * relSiz)
                LayoutManager.addConnection((True, False), el.getCore().getBody(), Rect(), (1.0, 0.0), (1.0, 0.0),
                                            offset=width, fixedGlobal=False, keepSizeFix=False)
                LayoutManager.addConnection((False, True), el.getCore().getBody(), self.getBody(), (0.0, 0.5), (0.0, 0.5))
                LayoutManager.addConnection((False, True), el.getCore().getBody(), Rect(), (0.0, 1.0), (0.0, 1.0),
                                            offset=self.__elementSizing[1], fixedGlobal=False, keepSizeFix=False)
                # align elements next to each other
                if idx == 0:
                    LayoutManager.addConnection((True, False), el.getCore().getBody(), self.getBody(), (0.0, 0.0), (0.0, 0.0))
                    totalWidth += width
                else:
                    LayoutManager.addConnection((True, False), el.getCore().getBody(), self._inner[idx-1].getCore().getBody(),
                                                (0.0, 0.0), (1.0, 0.0), offset=self.__offset)
                    totalWidth += width + self.__offset
            LayoutManager.addConnection((True, False), self.getBody(), Rect(), (1.0, 0.0), (0.0, 0.0), offset=totalWidth, fixedGlobal=False, keepSizeFix=False)
            LayoutManager.addConnection((False, True), self.getBody(), Rect(), (0.0, 1.0), (0.0, 0.0), offset=self.__elementSizing[1], fixedGlobal=False, keepSizeFix=False)


    def addElement(self, newElement: Element | tuple[Element, float]) -> None:
        """
        addElement adds a new element to the end of the stack.
        """
        if not isinstance(newElement, Element):
            self.__relativeSizing.append(newElement[1])
            newElement = newElement[0]
        else:
            self.__relativeSizing.append(1.0)
        self._inner.append(newElement)
        self._alignInner()

    def popElement(self):
        """
        popElement removes the last element from the stack.
        """
        if len(self._inner) > 0:
            self._inner.pop(-1)
            self.__relativeSizing.pop(-1)
            self._alignInner()

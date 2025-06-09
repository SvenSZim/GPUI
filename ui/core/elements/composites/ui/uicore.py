from typing import Any, override

from .....utility   import Rect
from ...elementcore import ElementCore
from ...element     import Element

class UICore(ElementCore):
    """
    UICore is the core object of the addon 'UI'.
    """
    __inner: list[Element]
    __offset: int
    __sizing: float

    __useHeader: bool
    __useFooter: bool

    __topBars: list[list[Element]]
    __numberOfTopBars: int
    __currentTopBar: int

    __bottomBars: list[list[Element]]
    __numberOfBottomBars: int
    __currentBottomBar: int

    __leftBars: list[list[Element]]
    __numberOfLeftBars: int
    __currentLeftBar: int

    __rightBars: list[list[Element]]
    __numberOfRightBars: int
    __currentRightBar: int

    def __init__(self, useheader: bool, usefooter: bool, inner: list[Element], offset: int=0, sizing: float=1.0) -> None:
        ElementCore.__init__(self, Rect())
        self.__inner    = inner
        self.__offset   = offset
        self.__sizing   = sizing
        self.__useHeader = useheader
        self.__useFooter =usefooter

        self.alignInner()

    def alignInner(self) -> None:
        self.__topBars      = []
        self.__numberOfTopBars      = 0
        self.__currentTopBar        = 0
        self.__bottomBars   = []
        self.__numberOfBottomBars   = 0
        self.__currentBottomBar     = 0
        self.__leftBars     = []
        self.__numberOfLeftBars     = 0
        self.__currentLeftBar       = 0
        self.__rightBars    = []
        self.__numberOfRightBars    = 0
        self.__currentRightBar      = 0

        if self.isZero():
            return
        
        elementSize: tuple[int, int] = (int(self.getWidth()/6 * self.__sizing), int(50 * self.__sizing))
        topBarHeight: int = int(elementSize[1] * 1.4)
        bottomBarHeight: int = int(elementSize[1] * 1.1)
        barSizes: list[Rect]
        usedInner: int = 0

        if self.__useHeader and self.__useFooter and len(self.__inner) > 1:
            barSizes = [
                Rect(                                                        size=(self.getWidth(), topBarHeight)),                                 # topbar
                Rect(topleft=(0,          self.getBottom()-bottomBarHeight), size=(self.getWidth(), bottomBarHeight)),                              # bottombar
                Rect(topleft=(self.getRight()-elementSize[0], topBarHeight), size=(elementSize[0], self.getHeight()-topBarHeight-bottomBarHeight)), # rightbar
                Rect(topleft=(0,                              topBarHeight), size=(elementSize[0], self.getHeight()-topBarHeight-bottomBarHeight)), # leftbar
            ]
            header: Element = self.__inner[0]
            header.align(barSizes[0])
            header.alignSize(barSizes[0])
            self.__topBars.append([header])
            self.__numberOfTopBars += 1
            footer: Element = self.__inner[1]
            footer.align(barSizes[1])
            footer.alignSize(barSizes[1])
            self.__bottomBars.append([footer])
            self.__numberOfBottomBars += 1
            usedInner += 2
        elif self.__useHeader:
            bottomBarHeight = 0
            barSizes = [
                Rect(                                                        size=(self.getWidth(), topBarHeight)),                                 # topbar
                Rect(topleft=(0,          self.getBottom()-bottomBarHeight), size=(self.getWidth(), bottomBarHeight)),                              # bottombar
                Rect(topleft=(self.getRight()-elementSize[0], topBarHeight), size=(elementSize[0], self.getHeight()-topBarHeight-bottomBarHeight)), # rightbar
                Rect(topleft=(0,                              topBarHeight), size=(elementSize[0], self.getHeight()-topBarHeight-bottomBarHeight)), # leftbar
            ]
            header: Element = self.__inner[0]
            header.align(barSizes[0])
            header.alignSize(barSizes[0])
            self.__topBars.append([header])
            self.__numberOfTopBars += 1
            usedInner += 1
        elif self.__useFooter:
            topBarHeight = 0
            barSizes = [
                Rect(                                                        size=(self.getWidth(), topBarHeight)),                                 # topbar
                Rect(topleft=(0,          self.getBottom()-bottomBarHeight), size=(self.getWidth(), bottomBarHeight)),                              # bottombar
                Rect(topleft=(self.getRight()-elementSize[0], topBarHeight), size=(elementSize[0], self.getHeight()-topBarHeight-bottomBarHeight)), # rightbar
                Rect(topleft=(0,                              topBarHeight), size=(elementSize[0], self.getHeight()-topBarHeight-bottomBarHeight)), # leftbar
            ]
            footer: Element = self.__inner[0]
            footer.align(barSizes[1])
            footer.alignSize(barSizes[1])
            self.__bottomBars.append([footer])
            self.__numberOfBottomBars += 1
            usedInner += 1
        else:
            topBarHeight = 0
            bottomBarHeight = 0
            barSizes = [
                Rect(                                                        size=(self.getWidth(), topBarHeight)),                                 # topbar
                Rect(topleft=(0,          self.getBottom()-bottomBarHeight), size=(self.getWidth(), bottomBarHeight)),                              # bottombar
                Rect(topleft=(self.getRight()-elementSize[0], topBarHeight), size=(elementSize[0], self.getHeight()-topBarHeight-bottomBarHeight)), # rightbar
                Rect(topleft=(0,                              topBarHeight), size=(elementSize[0], self.getHeight()-topBarHeight-bottomBarHeight)), # leftbar
            ]
        
        barSizes: list[Rect]        = [barSizes[2], barSizes[3]]
        verticalBar: list[bool]     = [True, True]
        maxSizes: list[int]         = [bar.getHeight() if vert else bar.getWidth() for bar, vert in zip(barSizes, verticalBar)]
        bars: list[list[Element]]   = [[] for _ in barSizes]
        cSizes: list[int]           = [0 for _ in barSizes]
        
        for el in self.__inner[usedInner:]:
            el.setActive(False)
            elSize: tuple[int, int] = el.getInnerSizing(elementSize)
            wasAdded: bool = False
            for idx, (barSize, vertBar, maxSize, bar, cSize) in enumerate(zip(barSizes, verticalBar, maxSizes, bars, cSizes)):
                if elSize[int(vertBar)] + cSize <= maxSize:
                    if vertBar:
                        el.align(barSize, offset=(0, cSize))
                        el.alignSize(Rect(size=(barSize.getWidth(), elSize[1])))
                    else:
                        el.align(barSize, offset=(cSize, 0))
                        el.alignSize(Rect(size=(elSize[0], barSize.getHeight())))
                    cSizes[idx] += elSize[int(vertBar)]
                    bar.append(el)
                    wasAdded = True
                    break
            if not wasAdded:
                #TODO
                print('could not add element!')
                print(maxSizes)
                print(elSize)

        self.__leftBars.append(bars[1])
        self.__numberOfLeftBars += 1
        self.__rightBars.append(bars[0])
        self.__numberOfRightBars += 1
        
        self.setTopBar(0)
        self.setBottomBar(0)
        self.setLeftBar(0)
        self.setRightBar(0)

    # -------------------- getter --------------------

    @override
    def getInnerSizing(self, elSize: tuple[int, int], args: dict[str, Any]) -> tuple[int, int]:
        return self.getSize()

    def getTopBar(self) -> list[Element]:
        if not self.__numberOfTopBars:
            return []
        return self.__topBars[self.__currentTopBar]

    def getBottomBar(self) -> list[Element]:
        if not self.__numberOfBottomBars:
            return []
        return self.__bottomBars[self.__currentBottomBar]

    def getLeftBar(self) -> list[Element]:
        if not self.__numberOfLeftBars:
            return []
        return self.__leftBars[self.__currentLeftBar]

    def getRightBar(self) -> list[Element]:
        if not self.__numberOfRightBars:
            return []
        return self.__rightBars[self.__currentRightBar]

    def getBars(self) -> tuple[list[Element], list[Element], list[Element], list[Element]]:
        return (self.getTopBar(), self.getBottomBar(), self.getLeftBar(), self.getRightBar())

    def getCurrentElements(self) -> list[Element]:
        els: list[Element] = [x for x in self.getTopBar()]
        els.extend(self.getBottomBar())
        els.extend(self.getLeftBar())
        els.extend(self.getRightBar())
        return els

    # -------------------- setter --------------------

    def setTopBar(self, idx: int) -> None:
        idx = abs(idx)
        if idx < self.__numberOfTopBars:
            for bar in self.__topBars:
                for el in bar:
                    el.setActive(False)
            for el in self.__topBars[idx]:
                el.setActive(True)
            self.__currentTopBar = idx

    def setBottomBar(self, idx: int) -> None:
        idx = abs(idx)
        if idx < self.__numberOfBottomBars:
            for bar in self.__bottomBars:
                for el in bar:
                    el.setActive(False)
            for el in self.__bottomBars[idx]:
                el.setActive(True)
            self.__currentBottomBar = idx
    
    def setLeftBar(self, idx: int) -> None:
        idx = abs(idx)
        if idx < self.__numberOfLeftBars:
            for bar in self.__leftBars:
                for el in bar:
                    el.setActive(False)
            for el in self.__leftBars[idx]:
                el.setActive(True)
            self.__currentLeftBar = idx
    
    def setRightBar(self, idx: int) -> None:
        idx = abs(idx)
        if idx < self.__numberOfRightBars:
            for bar in self.__rightBars:
                for el in bar:
                    el.setActive(False)
            for el in self.__rightBars[idx]:
                el.setActive(True)
            self.__currentRightBar = idx
    
    # -------------------- active-state --------------------

    def setActive(self, active: bool) -> None:
        if active:
            self.setTopBar(self.__currentTopBar)
            self.setBottomBar(self.__currentBottomBar)
            self.setLeftBar(self.__currentLeftBar)
            self.setRightBar(self.__currentRightBar)
        else:
            for el in self.__inner:
                el.setActive(False)

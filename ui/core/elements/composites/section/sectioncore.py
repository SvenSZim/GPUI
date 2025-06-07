from typing import Any, Optional, override

from .....utility   import Rect, AlignType
from .....interaction   import InputEvent, InputManager
from ...element     import Element
from ...elementcore import ElementCore

from ...atoms           import Box

class SectionCore(ElementCore):
    """
    SectionCore is the core object of the addon 'Section'.
    """
    ___vbox: Box
    _buttonActive: bool
    
    __header: Optional[tuple[Element, float]]
    __headersep: Optional[Element]
    __footer: Optional[tuple[Element, float]]
    __footersep: Optional[Element]

    __inner: list[tuple[Element, float]]
    __innerLimit: float
    __offset: int
    
    __sections: dict[int, list[Element]]
    __sectionAmount: int
    __currentSection: int

    __prevButton: Element
    __nextButton: Element

    def __init__(self, header: Optional[tuple[Element, float]], footer: Optional[tuple[Element, float]], buttons: tuple[Element, Element],
                 inner: list[tuple[Element, float]], separators: tuple[Optional[Element], Optional[Element]]=(None, None), innerLimit: float=5.0, offset: int=0) -> None:
        ElementCore.__init__(self, Rect())
        self._buttonActive = True

        self.__header = header
        self.__headersep = separators[0]
        self.__footer = footer
        self.__footersep = separators[1]
        
        self.__prevButton = buttons[0]
        self.__prevButton.set({'content':'Prev'})
        self.__nextButton = buttons[1]
        self.__nextButton.set({'content':'Next'})
        self.__prevButton.set({'quickSubscribeToClick':(self.prevSection, [])})
        self.__nextButton.set({'quickSubscribeToClick':(self.nextSection, [])})

        self.__inner = inner
        self.__innerLimit = innerLimit
        self.__offset = offset

        self.__currentSection = 0
        self._alignInner()

        InputManager.quickSubscribe(InputEvent.ARR_LEFT, self.prevSection)
        InputManager.quickSubscribe(InputEvent.ARR_RIGHT, self.nextSection)


    def _alignInner(self) -> None:
        self.___vbox = Box.parseFromArgs({})
        self.___vbox.align(self, offset=(0, -int(0.5*self.__offset)))
        self.___vbox.alignSize(self, absoluteOffset=(0, self.__offset))

        totalRelHeight: float = max(1, self.getTotalRelHeight())
        currentRelHeight: float = 0.0
        if self.__header:
            self.__header[0].align(self.___vbox, offset=(0, int(0.5*self.__offset)))
            self.__header[0].alignSize(self.___vbox, relativeAlign=(1, self.__header[1]/totalRelHeight), absoluteOffset=(0, -self.__offset))
            if self.__headersep:
                self.__headersep.alignpoint(self.___vbox, otherPoint=(0, self.__header[1]/totalRelHeight))
                self.__headersep.alignSize(self.___vbox, alignY=False)
            currentRelHeight += self.__header[1]
        elif self.__headersep:
            self.__headersep.setActive(False)

        idx: int = 0
        self.__sections: dict[int, list[Element]] = {0:[]}
        self.__sectionAmount: int = 0
        cRelHeight: float = 0.0
        while idx < len(self.__inner):
            el: Element = self.__inner[idx][0]
            el.setActive(False)
            relHeight: float = self.__inner[idx][1] * self.__inner[idx][0].getInnerSizing((1,1))[1]
            if relHeight <= self.__innerLimit:
                if cRelHeight + relHeight > self.__innerLimit:
                    cRelHeight = 0.0
                    self.__sectionAmount += 1
                    self.__sections[self.__sectionAmount] = [el]
                else:
                    self.__sections[self.__sectionAmount].append(el)

                el.alignpoint(self.___vbox, otherPoint=(0, (currentRelHeight + cRelHeight)/totalRelHeight), offset=(0, int(0.5*self.__offset)))
                cRelHeight += relHeight
                el.alignSize(self.___vbox, relativeAlign=(1, relHeight/totalRelHeight), absoluteOffset=(0, -self.__offset))
            idx += 1
        self.__sectionAmount += 1
        self.setSection(0)

        if self.__footer:
            self.__footer[0].align(self.___vbox, AlignType.iBiR, offset=(0, int(-0.5*self.__offset)))
            self.__footer[0].alignSize(self.___vbox, relativeAlign=(1, self.__footer[1]/totalRelHeight), absoluteOffset=(0, -self.__offset))
            if self.__footersep:
                self.__footersep.alignpoint(self.___vbox, otherPoint=(0, 1-self.__footer[1]/totalRelHeight))
                self.__footersep.alignSize(self.___vbox, alignY=False)
        elif self.__footersep:
            self.__footersep.setActive(False)

        if not self.__sectionAmount:
            self.__prevButton.setActive(False)
            self.__nextButton.setActive(False)
        else:
            self.__prevButton.setActive(True)
            self.__nextButton.setActive(True)
            if self.__footer is not None:
                self.__prevButton.alignpoint(self.___vbox, otherPoint=(0, 1-self.__footer[1]/self.getTotalRelHeight()))
                self.__prevButton.alignSize(self, relativeAlign=(0.15, min(0.8, self.__footer[1])/self.getTotalRelHeight()))
                self.__nextButton.alignpoint(self.___vbox, myPoint=(1,0), otherPoint=(1, 1-self.__footer[1]/self.getTotalRelHeight()))
                self.__nextButton.alignSize(self, relativeAlign=(0.15, min(0.8, self.__footer[1])/self.getTotalRelHeight()))
            elif self.__header is not None:
                self.__prevButton.alignpoint(self.___vbox, myPoint=(0,1), otherPoint=(0, self.__header[1]/self.getTotalRelHeight()))
                self.__prevButton.alignSize(self, relativeAlign=(0.15, min(0.8, self.__header[1])/self.getTotalRelHeight()))
                self.__nextButton.alignpoint(self.___vbox, myPoint=(1,1), otherPoint=(1, self.__header[1]/self.getTotalRelHeight()))
                self.__nextButton.alignSize(self, relativeAlign=(0.15, min(0.8, self.__header[1])/self.getTotalRelHeight()))
            else:
                self.__prevButton.align(self.___vbox, AlignType.iBiL, offset=(0, int(-0.5*self.__offset)))
                self.__prevButton.alignSize(self, relativeAlign=(0.15, min(0.8, self.getTotalRelHeight())/self.getTotalRelHeight()))
                self.__nextButton.align(self.___vbox, AlignType.iBiR, offset=(0, int(-0.5*self.__offset)))
                self.__nextButton.alignSize(self, relativeAlign=(0.15, min(0.8, self.getTotalRelHeight())/self.getTotalRelHeight()))

    # -------------------- getter --------------------

    def getTotalRelHeight(self) -> float:
        return (self.__header[1] if self.__header is not None else 0.0) + \
               self.__innerLimit + \
               (self.__footer[1] if self.__footer is not None else 0.0)

    def getVBox(self) -> Box:
        return self.___vbox

    @override
    def getInnerSizing(self, elSize: tuple[int, int], args: dict[str, Any]) -> tuple[int, int]:
        maxX: int = 0
        maxY: int = 0
        totY: int = 0
        for (el, _) in self.__inner:
            cX, cY = el.getInnerSizing(elSize, args)
            maxX, maxY = max(maxX, cX), max(maxY, cY)
            totY += cY
        if 'sec_max' in args:
            return maxX, maxY
        if 'sec_tot' in args:
            return maxX, totY
        return maxX, int(self.getTotalRelHeight() * elSize[1])

    def getHeader(self) -> Optional[Element]:
        return self.__header[0] if self.__header is not None else None

    def getSeparators(self) -> tuple[Optional[Element], Optional[Element]]:
        return self.__headersep, self.__footersep

    def getFooter(self) -> Optional[Element]:
        return self.__footer[0] if self.__footer is not None else None

    def getInner(self) -> list[Element]:
        return [x[0] for x in self.__inner]

    def getCurrentSectionElements(self) -> list[Element]:
        return self.__sections[self.__currentSection]

    def getButtons(self) -> list[Element]:
        return [x for x in [self.__prevButton, self.__nextButton] if x is not None]

    # -------------------- setter --------------------

    def setInnerLimit(self, newLimit: float) -> None:
        self.__innerLimit = abs(newLimit)
        self._alignInner()

    def setSection(self, section: int) -> None:
        for el in self.getCurrentSectionElements():
            el.setActive(False)
        self.__currentSection = max(0, min(section, self.__sectionAmount-1))
        for el in self.getCurrentSectionElements():
            el.setActive(True)

    def prevSection(self) -> None:
        if self._buttonActive:
            if self.getRect().collidepoint(InputManager.getMousePosition()):
                self.setSection((self.__currentSection - 1) % self.__sectionAmount)

    def nextSection(self) -> None:
        if self._buttonActive:
            if self.getRect().collidepoint(InputManager.getMousePosition()):
                self.setSection((self.__currentSection + 1) % self.__sectionAmount)
    
    # -------------------- active-state --------------------

    def setActive(self, active: bool) -> None:
        self._buttonActive = active
        if self.__header is not None:
            self.__header[0].setActive(active)
            if self.__headersep:
                self.__headersep.setActive(active)
        if not active:
            for (el, _) in self.__inner:
                el.setActive(active)
        else:
            self.setSection(self.__currentSection)
        if self.__footer is not None:
            self.__footer[0].setActive(active)
            if self.__footersep:
                self.__footersep.setActive(active)
        if self.__prevButton is not None:
            self.__prevButton.setActive(active)
        if self.__nextButton is not None:
            self.__nextButton.setActive(active)

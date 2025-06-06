from dataclasses import dataclass
from typing import override

from ....utility import Rect, iRect, AlignType
from ....interaction import EventManager

@dataclass
class RelPoint:
    isGlobal: bool
    myP: float
    otherP: float
    offset: int
    other: iRect

@dataclass
class RelativePoints:
    dim: int # 0: x, 1: y
    relpoint1: RelPoint # newest
    relpoint2: RelPoint

    def setRelpoint(self, ref: iRect, myP: float, otherP: float, offset: int=0, globalFix: bool=True, keepSize: bool=True):
        if not (not self.relpoint2.isGlobal and keepSize or not globalFix and not self.relpoint1.isGlobal or (self.relpoint1.isGlobal and globalFix and self.relpoint1.myP == myP)):
            # Exclude: overwriting local fix if keepSize, 2 local fixes, fixing same point twice
            self.relpoint2 = self.relpoint1
        self.relpoint1 = RelPoint(globalFix, myP, otherP, offset, ref)

    def getDimension(self) -> tuple[int, int]:
        """
        getDimension returns the start pos and the length of the 'line' defined
        by the stored points.

        Returns (tuple[int, int]): (start, length) ~ the 'line' defined by the points.
        """
        abspos1: int
        if self.relpoint1.isGlobal:
            abspos1 = int(self.relpoint1.other.getPoint((self.relpoint1.otherP, self.relpoint1.otherP))[self.dim] + self.relpoint1.offset)
        else:
            abspos1 = int(self.relpoint1.other.getSize()[self.dim] * self.relpoint1.otherP + self.relpoint1.offset)
        abspos2: int
        if self.relpoint2.isGlobal:
            abspos2 = int(self.relpoint2.other.getPoint((self.relpoint2.otherP, self.relpoint2.otherP))[self.dim] + self.relpoint2.offset)
        else:
            abspos2 = int(self.relpoint2.other.getSize()[self.dim] * self.relpoint2.otherP + self.relpoint2.offset)

        
        length: int = 0
        start: int = 0
        if self.relpoint1.isGlobal and self.relpoint2.isGlobal:
            length = int((abspos2 - abspos1) / (self.relpoint2.myP - self.relpoint1.myP))
            start = int(abspos1 - length * self.relpoint1.myP)
        elif self.relpoint1.isGlobal:
            length = int(abspos2 / self.relpoint2.myP)
            start = int(abspos1 - length * self.relpoint1.myP)
        else:
            length = int(abspos1 / self.relpoint1.myP)
            start = int(abspos2 - length * self.relpoint2.myP)
        return (start, max(0,length))
            

Point = tuple[float, float]

class Body(iRect):
    """
    Body is a more advanced class for storing and manipulating a rectangle.
    It extends the Rect class and works by additionaly storing fixpoints which fix
    relative positions of the body to fixed coordinates. These can then be used to
    calculte the actual rect of the body.
    """
    __resetBodyUpdateStatusEvent: str = EventManager.createEvent()
    __updateBodyEvent: str = EventManager.createEvent()
    __updateLayoutEvent: str = EventManager.createEvent()

    __updating: bool
    __updated: bool

    __setXRelations: RelativePoints
    __setYRelations: RelativePoints

    __position: tuple[int, int]
    __size: tuple[int, int]

    # -------------------- static --------------------

    @staticmethod
    def getLayoutUpdateEvent() -> str:
        return Body.__updateLayoutEvent

    @staticmethod
    def updateBodys() -> None:
        EventManager.triggerEvent(Body.__resetBodyUpdateStatusEvent)
        EventManager.triggerEvent(Body.__updateBodyEvent)

    # -------------------- creation --------------------

    def __init__(self, rect: Rect=Rect()) -> None:
        super().__init__()

        EventManager.quickSubscribe(Body.__resetBodyUpdateStatusEvent, self.__unsetUpdated)
        EventManager.quickSubscribe(Body.__updateBodyEvent, self.update)

        self.__setXRelations = RelativePoints(0, RelPoint(False, 1.0, 1.0, 0, rect), RelPoint(True, 0.0, 0.0, 0, rect))
        self.__setYRelations = RelativePoints(1, RelPoint(False, 1.0, 1.0, 0, rect), RelPoint(True, 0.0, 0.0, 0, rect))

        self.__updateDimensions()

    def __updateDimensions(self) -> None:
        self.__updating = True

        dimX = self.__setXRelations.getDimension()
        dimY = self.__setYRelations.getDimension()

        self.__position = (dimX[0], dimY[0])
        self.__size = (dimX[1], dimY[1])
        self.__updated = True
        self.__updating = False

    def copy(self) -> 'Body':
        return Body()


    # -------------------- iRect-implementation --------------------

    @override
    def getSize(self) -> tuple[int, int]:
        """
        getSize returns the size of the element.

        Returns (tuple[int, int]) ~ (width, height): size of the element
        """
        if self.__updated:
            return self.__size
        if self.__updating:
            raise ReferenceError('UI Layout references itself!')
        
        self.update()

        return self.__size

    @override
    def getPosition(self) -> tuple[int, int]:
        """
        getPosition return the position of the element.

        Returns (tuple[int, int]) ~ (x-pos, y-pos): position of the element
        """
        if self.__updated:
            return self.__position
        if self.__updating:
            raise ReferenceError('UI Layout references itself!')
        
        self.update()

        return self.__position

    # -------------------- additional-getter --------------------

    def getRect(self) -> Rect:
        """
        getRect returns the position and size of the element stored in a Rect object

        Returns (Rect): Rect object containing the pos and size of the element
        """
        return Rect(self.__position, self.__size)

    # -------------------- positional-setter --------------------

    def __unsetUpdated(self) -> None:
        self.__updated = False

    def update(self) -> None:
        if not self.__updated:
            self.__updateDimensions()

    def forceUpdate(self) -> None:
        self.__updated = False
        self.update()

    def addReferenceConnection(self, other: iRect, connectionDimension: tuple[bool, bool],
                        myFixPoint: Point, otherFixPoint: Point, offset: tuple[int, int]=(0,0),
                        fixedGlobal: tuple[bool, bool]=(True, True), keepSize: tuple[bool, bool]=(True, True)) -> None:
        """
        applyConnection is a function to set a new connection of the body.
        (should only be accessed by the LayoutManager)

        Args:
            other               (iRect)                                 : the coordinates to use for fixing
            connectionDimension (tuple[bool, bool]) ~ (x-axis, y-axis)  : the dimensions to use when fixing
            myFixPoint          (Point) ~ tuple[float, float]           : the relative positions of the body to fix
            otherFixPoint       (Point) ~ tuple[float, float]           : the relative positions of the other rect to use as fixed coordinates
            offset              (tuple[int, int])                       : a offset to use when fixing. int applys to all dimensions
            fixedGlobal         (tuple[bool, bool])                     : boolean if the fixations are global positioned or locally
                                                                            (in reference to the object itself)
            keepSize            (tuple[bool, bool])                     : boolean if the fixations should keep relative-fixes and just
                                                                            override global fixes
        """
        # set new x-axis fixpoints
        if connectionDimension[0]:
            self.__setXRelations.setRelpoint(other, myFixPoint[0], otherFixPoint[0], offset=offset[0], globalFix=fixedGlobal[0], keepSize=keepSize[0])

        # set new y-axis fixpoints
        if connectionDimension[1]:
            self.__setYRelations.setRelpoint(other, myFixPoint[1], otherFixPoint[1], offset=offset[1], globalFix=fixedGlobal[1], keepSize=keepSize[1])
    
    
    def align(self, alignagainst: iRect, align: AlignType, alignX: bool=True, alignY: bool=True,
              offset: tuple[int, int]=(0, 0), keepSize: bool=True) -> None:
        """
        align creates a LayoutRequest to align the element with the given one.

        Args:
            other   (Element or Core or Rect)   : the reference to align against
            align   (Align)                     : the type of alignment to use
        """
        kSize: tuple[bool, bool] = (keepSize, keepSize)
        xalign, xi, yalign, yi = (align.value & 0b11, (align.value & 0b100) >> 2, (align.value & 0b11000) >> 3, (align.value & 0b100000) >> 5)
        if alignX:
            if xi:
                self.addReferenceConnection(alignagainst, (True, False), (xalign * 0.5, 0.0), (xalign * 0.5, 0.0), offset=offset, keepSize=kSize)
            else:
                self.addReferenceConnection(alignagainst, (True, False), ((2 - xalign) * 0.5, 0.0), (xalign * 0.5, 0.0), offset=(offset[0], offset[1]), keepSize=kSize)
        if alignY:
            if yi:
                self.addReferenceConnection(alignagainst, (False, True), (0.0, yalign * 0.5), (0.0, yalign * 0.5), offset=offset, keepSize=kSize)
            else:
                self.addReferenceConnection(alignagainst, (False, True), (0.0, (2 - yalign) * 0.5), (0.0, yalign * 0.5), offset=(offset[0], offset[1]), keepSize=kSize)


EventManager.quickSubscribe(Body.getLayoutUpdateEvent(), Body.updateBodys)

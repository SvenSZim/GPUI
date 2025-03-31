from dataclasses import dataclass
from typing import override

from .....utility import Rect, iRect

@dataclass
class GlobalFix:
    """
    GlobalFix is a dataclass to store information
    about a global fix of a relative-position to a
    absolute coordinate in a single dimension.
    """
    relativePosition: float
    absolutePosition: int

@dataclass
class LocalFix:
    """
    LocalFix is a dataclass to store information
    about a local fixed offset-position to a absolute 
    offset in a single dimension.
    """
    relativePosition: float
    absolutePosition: int

@dataclass
class FixedPoints:
    """
    FixedPoints is a dataclass to store the defining size
    and position information for a rectangle in one dimension.
    """

    fixpoint1: GlobalFix | LocalFix # first fixpoint
    fixpoint2: GlobalFix            # second fixpoint (there cant be 2 local fixes)

    def setFixPoint(self, newFix: GlobalFix | LocalFix, keepSizeFix: bool=True):
        """
        setFixPoint sets a new fixpoint in the set dimension.

        Args:
            newFix   (GlobalFix | LocalFix): the new fixpoint to store.
            keepSize (bool)                : boolean if the localfix should be kept
        """
        if isinstance(newFix, LocalFix):
            if newFix.relativePosition != 0.0: # there cant be a local fix with relativePos = 0
                self.fixpoint1 = newFix
        else:
            if not (isinstance(self.fixpoint1, LocalFix) and keepSizeFix) and \
              self.fixpoint2.relativePosition != newFix.relativePosition:
                self.fixpoint1 = self.fixpoint2
            self.fixpoint2 = newFix


    def getDimension(self) -> tuple[int, int]:
        """
        getDimension returns the start pos and the length of the 'line' defined
        by the stored fix-points.

        Returns (tuple[int, int]): (start, length) ~ the 'line' defined by the fix-points.
        """
        length: int = 0
        start: int = 0
        # check for local positioned fixes
        if isinstance(self.fixpoint1, LocalFix):
            length = int(self.fixpoint1.absolutePosition / self.fixpoint1.relativePosition)
            start = int(self.fixpoint2.absolutePosition - length * self.fixpoint2.relativePosition)
        else:
            length = int((self.fixpoint2.absolutePosition - self.fixpoint1.absolutePosition) / 
                         (self.fixpoint2.relativePosition - self.fixpoint1.relativePosition))
            start = int(self.fixpoint1.absolutePosition - length * self.fixpoint1.relativePosition)
        return (start, length)


Point = tuple[float, float]

class Body(iRect):
    """
    Body is a more advanced class for storing and manipulating a rectangle.
    It extends the Rect class and works by additionaly storing fixpoints which fix
    relative positions of the body to fixed coordinates. These can then be used to
    calculte the actual rect of the body.
    """

    # fixed points are relative positions of the body that are fixed to a fixed coordinate
    __fixedXPoints: FixedPoints
    __fixedYPoints: FixedPoints

    # -------------------- creation --------------------

    def __init__(self, rect: Rect=Rect()) -> None:
        """
        Body objects should only be created by the BodyManager!!!
        (because they need to be registered in the LayoutManager)
        """
        super().__init__()

        self.__fixedXPoints = FixedPoints(LocalFix(1.0, rect.width), GlobalFix(0.0, rect.left))
        self.__fixedYPoints = FixedPoints(LocalFix(1.0, rect.height), GlobalFix(0.0, rect.top))

    # -------------------- iRect-implementation --------------------

    @override
    def getSize(self) -> tuple[int, int]:
        """
        getSize returns the size of the element.

        Returns (tuple[int, int]) ~ (width, height): size of the element
        """
        return (self.__fixedXPoints.getDimension()[1], self.__fixedYPoints.getDimension()[1])

    @override
    def getPosition(self) -> tuple[int, int]:
        """
        getPosition return the position of the element.

        Returns (tuple[int, int]) ~ (x-pos, y-pos): position of the element
        """
        return (self.__fixedXPoints.getDimension()[0], self.__fixedYPoints.getDimension()[0])

    # -------------------- additional-getter --------------------

    def getRect(self) -> Rect:
        """
        getRect returns the position and size of the element stored in a Rect object

        Returns (Rect): Rect object containing the pos and size of the element
        """
        left, width = self.__fixedXPoints.getDimension()
        top, height = self.__fixedYPoints.getDimension()
        return Rect((left, top), (width, height))
        
    def setRect(self, rect: Rect) -> None:
        """
        setRect force-sets the rect of the body object.

        Args:
            rect (Rect): the rect to be stored.
        """
        self.__fixedXPoints.setFixPoint(GlobalFix(0.0, rect.left))
        self.__fixedXPoints.setFixPoint(LocalFix(1.0, rect.width))
        self.__fixedYPoints.setFixPoint(GlobalFix(0.0, rect.top))
        self.__fixedYPoints.setFixPoint(LocalFix(1.0, rect.height))

    # -------------------- positional-setter --------------------

    def applyConnection(self, other: iRect, connectionDimension: tuple[bool, bool],
                        myFixPoint: Point, otherFixPoint: Point, offset: int | tuple[int, int],
                        fixedGlobal: tuple[bool, bool]=(True, True), keepSizeFix: tuple[bool, bool]=(True, True)) -> None:
        """
        applyConnection is a function to set a new connection of the body.
        (should only be accessed by the LayoutManager)

        Args:
            other               (iRect)                                 : the coordinates to use for fixing
            connectionDimension (tuple[bool, bool]) ~ (x-axis, y-axis)  : the dimensions to use when fixing
            myFixPoint          (Point) ~ tuple[float, float]           : the relative positions of the body to fix
            otherFixPoint       (Point) ~ tuple[float, float]           : the relative positions of the other rect to use as fixed coordinates
            offset              (int or tuple[int, int])                : a offset to use when fixing. int applys to all dimensions
            fixedGlobal         (tuple[bool, bool])                     : boolean if the fixations are global positioned or locally
                                                                            (in reference to the object itself)
            keepSizeFix         (tuple[bool, bool])                     : boolean if the fixations should keep relative-fixes and just
                                                                            override global fixes
        """
        newX: int = int(other.getLeft() + otherFixPoint[0] * other.getWidth() )
        newY: int = int(other.getTop()  + otherFixPoint[1] * other.getHeight())
        
        # apply offset
        if isinstance(offset, int):
            newX += offset
            newY += offset
        else:
            newX += offset[0]
            newY += offset[1]
        
        # set new x-axis fixpoints
        if connectionDimension[0]:
            if fixedGlobal[0]:
                self.__fixedXPoints.setFixPoint(GlobalFix(myFixPoint[0], newX), keepSizeFix=keepSizeFix[0])
            else:
                self.__fixedXPoints.setFixPoint(LocalFix(myFixPoint[0], newX), keepSizeFix=keepSizeFix[0])

        # set new y-axis fixpoints
        if connectionDimension[1]:
            if fixedGlobal[1]:
                self.__fixedYPoints.setFixPoint(GlobalFix(myFixPoint[1], newY), keepSizeFix=keepSizeFix[1])
            else:
                self.__fixedYPoints.setFixPoint(LocalFix(myFixPoint[1], newY), keepSizeFix=keepSizeFix[1])

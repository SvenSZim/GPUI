from dataclasses import dataclass
from typing import override

from ....utility import Rect, iRect, AlignType
from ....interaction import EventManager

@dataclass
class RelPoint:
    """A relative point that defines a positional relationship between two rectangles.
    
    This class represents a point that can be either globally fixed (absolute position)
    or relatively fixed (percentage of size) to another rectangle.
    
    Attributes:
        isGlobal (bool): True if the point is fixed in global coordinates, False if relative
        myP (float): The relative position on this rectangle (0.0 to 1.0)
        otherP (float): The relative position on the reference rectangle (0.0 to 1.0)
        offset (int): Additional pixel offset to apply to the calculated position
        other (iRect): Reference rectangle used for position calculation
    """
    isGlobal: bool
    myP: float
    otherP: float
    offset: int
    other: iRect

@dataclass
class RelativePoints:
    """Manages two relative points that define a dimension (width or height) of a rectangle.
    
    This class maintains two RelPoint instances that together define either the width (x-axis)
    or height (y-axis) of a rectangle. It handles the logic for updating relative positions
    while preserving size constraints.
    
    Attributes:
        dim (int): Dimension indicator - 0 for x-axis, 1 for y-axis
        relpoint1 (RelPoint): Most recently set relative point
        relpoint2 (RelPoint): Previously set relative point
    
    Note:
        The two points are used to calculate both position and size in the given dimension.
        When both points are global, they directly define start and end positions.
        When one point is relative, it affects how size is calculated.
    """
    dim: int  # 0: x, 1: y
    relpoint1: RelPoint  # newest
    relpoint2: RelPoint

    def setRelpoint(self, ref: iRect, myP: float, otherP: float, offset: int=0, globalFix: bool=True, keepSize: bool=True):
        """Updates the relative point configuration for this dimension.
        
        This method manages the two relative points that define the rectangle's position
        and size in one dimension. It handles the logic for when to replace existing
        points and how to maintain size constraints.
        
        Args:
            ref (iRect): Reference rectangle to position against
            myP (float): Relative position on this rectangle (0.0 to 1.0)
            otherP (float): Relative position on reference rectangle (0.0 to 1.0)
            offset (int, optional): Pixel offset to add to calculated position. Defaults to 0.
            globalFix (bool, optional): If True, fixes in global coordinates. Defaults to True.
            keepSize (bool, optional): If True, preserves current size when possible. Defaults to True.
        
        Note:
            The method applies several rules to maintain layout stability:
            - Won't overwrite local fixes if keepSize is True
            - Prevents having two local fixes simultaneously
            - Avoids fixing the same point twice with global coordinates
        """
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
"""Type alias for a 2D point using relative coordinates (0.0 to 1.0 for each dimension)"""

class Body(iRect):
    """A sophisticated rectangle implementation with constraint-based positioning system.
    
    The Body class extends iRect by implementing a constraint-based positioning system
    that allows rectangles to be positioned and sized relative to other rectangles.
    It maintains a set of relative points (fix points) that define its position and
    size in relation to other rectangles in the layout.
    
    Features:
        - Constraint-based positioning using relative and absolute fix points
        - Automatic size calculation based on constraints
        - Circular dependency detection
        - Event-based update system for efficient layout recalculation
        - Alignment helpers for common positioning scenarios
    
    The positioning system uses two pairs of RelativePoints (one for x-axis, one for
    y-axis) to define the rectangle's position and size. Each pair can mix global
    (absolute) and relative positioning constraints.
    
    Example:
        ```python
        # Create a body that's 50% the width of another rect and aligned to its center
        ref_rect = Rect((0, 0), (400, 300))
        body = Body()
        body.align(ref_rect, AlignType.CENTER)
        body.addReferenceConnection(ref_rect, (True, False), 
                                  (0.0, 0.0), (0.25, 0.0),  # Fix left at 25% of ref
                                  (0, 0), (True, True))
        ```
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
        """Gets the event name used for layout update notifications.
        
        This event is triggered when the layout system needs to recalculate
        positions and sizes of all Body instances in the UI.
        
        Returns:
            str: The layout update event identifier
        """
        return Body.__updateLayoutEvent

    @staticmethod
    def updateBodys() -> None:
        """Triggers a global update of all Body instances.
        
        This method initiates a two-phase update process:
        1. Resets the update status of all bodies (allows detection of circular deps)
        2. Triggers the actual update calculation for all bodies
        
        Note:
            This is typically called when the layout needs to be recalculated,
            such as after window resizing or content changes.
        """
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
        """Creates a new empty Body instance.
        
        Returns:
            Body: A new Body instance with default initialization
        
        Note:
            This is a basic implementation that returns an empty Body.
            Subclasses should override to implement proper deep copying.
        """
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
        """Internal method to mark this body as needing an update.
        
        This is called during the first phase of the global update process
        to prepare all bodies for recalculation.
        """
        self.__updated = False

    def update(self) -> None:
        if not self.__updated:
            self.__updateDimensions()

    def forceUpdate(self) -> None:
        """Forces an immediate recalculation of this body's position and size.
        
        This method explicitly invalidates the current layout calculations
        and triggers an immediate update, regardless of the body's current
        update status. Use this when you need to ensure fresh calculations.
        """
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

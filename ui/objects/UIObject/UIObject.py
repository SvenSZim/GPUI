from enum import Enum
from typing import Optional

class AlignmentType(Enum):
    TopLeft = 0
    TopRight = 1
    BottomLeft = 2
    BottomRight = 3

class UIObjectBody():
    """
    Custom definition of object body as a rect which can be placed and scaled
    absolute or in relation to another object body element.
    This enables more flexibility when positioning multiple related elements
    on screen.
    """

    position: tuple[int | float, int | float]
    size: tuple[int | float, int | float]

    relativeObjectsPosition: tuple[Optional['UIObject'], Optional['UIObject']]
    relativeObjectsPositionType: tuple[AlignmentType, AlignmentType]
    relativeObjectsSize: tuple[Optional['UIObject'], Optional['UIObject']]
    
    topleft: tuple[int, int]
    width: int
    height: int


    def __init__(self, position: tuple[int | float, int | float], size: tuple[int | float, int | float],
                relativeObjectsPosition: tuple[Optional['UIObject'], Optional['UIObject']] = (None, None), 
                relativeObjectsPositionType: tuple[int, int] = (0, 0),
                relativeObjectsSize: tuple[Optional['UIObject'], Optional['UIObject']] = (None, None)) -> None:
        self.position = position
        self.size = size
        self.relativeObjectsPosition = relativeObjectsPosition
        self.relativeObjectsPositionType = (AlignmentType(relativeObjectsPositionType[0]), 
                                            AlignmentType(relativeObjectsPositionType[1]))
        self.relativeObjectsSize = relativeObjectsSize


    def getSize(self) -> tuple[int, int]:
        """
        Function that calculates the size of the UIObjectBody object.
        Two modes:
        1. Object is absolute sized: It just returns the absolute size of the object.
        2. Object is relative sized: 
            Size is calculated in respect to the parent UIObject(s) size(s).
            Given size is interpreted as either scale down of parent size (float)
            or reduction of parent size (int).
        
        If relative positioned:
            Calls the `getSize` method(s) from parent UIObject('s)

        Returns:
            tuple[int, int]: The size of the UIObject object
        """
        absoluteSizeX: int = 0
        absoluteSizeY: int = 0
        selfSizeX: int | float
        selfSizeY: int | float
        (selfSizeX, selfSizeY) = self.size

        #X-Size
        if self.relativeObjectsSize[0] is None:
            #absolute sized
            absoluteSizeX = int(selfSizeX)
        else:
            #relative sized
            relObjX: 'UIObject' = self.relativeObjectsSize[0]

            #modify parent size by given amount
            if isinstance(selfSizeX, int):
                #absolute amount ('offset')
                absoluteSizeX = int(relObjX.getSize()[0] + selfSizeX)
            else:
                #relative amount (fraction)
                if selfSizeX < 0:
                    #negative scale-down doesn't make sense
                    selfSizeX = -selfSizeX
                absoluteSizeX = int(relObjX.getSize()[0] * selfSizeX)

        #Y-Size
        if self.relativeObjectsSize[1] is None:
            #absolute sized
            absoluteSizeY = int(selfSizeY)
        else:
            #relative sized
            relObjY: 'UIObject' = self.relativeObjectsSize[1]

            #modify parent size by given amount
            if isinstance(selfSizeY, int):
                #absolute amount ('offset')
                absoluteSizeY = int(relObjY.getSize()[1] + selfSizeY)
            else:
                #relative amount (fraction)
                if selfSizeY < 0:
                    #negative scale-down doesn't make sense
                    selfSizeY = -selfSizeY
                absoluteSizeY = int(relObjY.getSize()[1] * selfSizeY)

        return (absoluteSizeX, absoluteSizeY)


    def getPosition(self) -> tuple[int, int]:
        """
        Function that calculates the position (top-left corner) of the UIObjectBody object.
        Two modes:
        1. Object is absolute positioned: It just returns the absolute position of the object.
        2. Object is relative positioned: 
            Position is calculated in respect to the parent UIObject(s) position
            and the corner connection given by the relativeObjectsPositionType:
                child-corner -> parent-corner
                top-left to top-left (0,0)
                top-left to top-right (0,1)
                ...
                bottom-left to bottom-right (2,3)
                ...
                bottom-right to bottom-right (3,3)
            Furthermore the given 'position' is interpreted as offset. (if float relative to parent size)

        If relative positioned:
            Calls the `getSize` method from this UIObjectBody
            Calls the `getPosition` method(s) from parent UIObject('s)
            Calls the `getSize` method(s) from parent UIObject('s)

        Returns:
            tuple[int, int]: The position of the top-left corner of the UIObject
        """
        absolutePosX: int = 0
        absolutePosY: int = 0
        selfPosX: int | float
        selfPosY: int | float
        (selfPosX, selfPosY) = self.position

        #X-Position
        if self.relativeObjectsPosition[0] is None:
            #absolute positioned
            absolutePosX = int(selfPosX)
        else:
            #relative positioned
            relObjX: 'UIObject' = self.relativeObjectsPosition[0]
            
            #interpret 'position' as offset
            if isinstance(selfPosX, int):
                absolutePosX += selfPosX
            else:
                #if float: relative to parent-size
                absolutePosX += int(selfPosX * relObjX.getSize()[0])
            
            #topleft: 0, topright: 1, bottomleft: 2, bottomright: 3
            absolutePosX += relObjX.getPosition()[0]
            connectionTypeChild: int = self.relativeObjectsPositionType[0].value
            connectionTypeParent: int = self.relativeObjectsPositionType[1].value
            connectionTypeLeftOrRightChild: int = connectionTypeChild % 2 # left: 0, right: 1
            connectionTypeLeftOrRightParent: int = connectionTypeParent % 2

            if connectionTypeLeftOrRightParent == 1:
                #use right edge of parent object
                absolutePosX += relObjX.getSize()[0]
            if connectionTypeLeftOrRightChild == 1:
                #use right edge of this object
                absolutePosX -= self.getSize()[0]
        
        #Y-Position
        if self.relativeObjectsPosition[1] is None:
            #absolute positioned
            absolutePosY = int(selfPosY)
        else:
            #relative positioned
            relObjY: 'UIObject' = self.relativeObjectsPosition[1]
            
            #interpret 'position' as offset
            if isinstance(selfPosY, int):
                absolutePosY += selfPosY
            else:
                #if float: relative to parent-size
                absolutePosY += int(selfPosY * relObjY.getSize()[1])
            
            #topleft: 0, topright: 1, bottomleft: 2, bottomright: 3
            absolutePosY += relObjY.getPosition()[1]
            connectionTypeChild: int = self.relativeObjectsPositionType[0].value
            connectionTypeParent: int = self.relativeObjectsPositionType[1].value
            connectionTypeTopOrBottomChild: int = connectionTypeChild // 2 # top: 0, bottom: 1
            connectionTypeTopOrBottomParent: int = connectionTypeParent // 2

            if connectionTypeTopOrBottomParent == 1:
                #use bottom edge of parent object
                absolutePosY += relObjY.getSize()[1]
            if connectionTypeTopOrBottomChild == 1:
                #use bottom edge of this object
                absolutePosY -= self.getSize()[1]

        return (absolutePosX, absolutePosY)

    def update(self) -> None:
        self.width, self.height = self.getSize()
        self.topleft = self.getPosition()




class UIObject():
    """
    UIObject is a abstract class to define functionality
    of UIObjects
    """
    
    active: bool
    body: 'UIObjectBody'

    def __init__(self, objectBody: 'UIObjectBody', active: bool=True) -> None:
        self.active = active
        self.body = objectBody
        UIObject.update(self) #explicitly calls the update function from UIObject (in case it gets overwritten)

    def isActive(self) -> bool:
        return self.active

    def setActive(self, active: bool) -> None:
        self.active = active

    def toggleActive(self) -> bool:
        self.active = not self.active
        return self.active

    def getSize(self) -> tuple[int, int]:
        return (self.body.width, self.body.height)

    def getPosition(self) -> tuple[int, int]:
        return self.body.topleft

    def update(self) -> None:
        self.body.update()

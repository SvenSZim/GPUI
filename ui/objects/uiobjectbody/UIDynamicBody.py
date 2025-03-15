from enum import Enum
from typing import Optional, override

from ..generic import Rect
from .UIABCBody import UIABCBody


class AlignmentType(Enum):
    """
    AlignmentType is used to store the positioning relation between two
    UIBody elements.
    """
    TOP_LEFT = 0
    TOP_RIGHT = 1
    BOTTOM_LEFT = 2
    BOTTOM_RIGHT = 3

class UIDynamicBody(UIABCBody):
    """
    UIDynamicBody is a custom definition of object body as a rect
    which can be placed and scaled absolute or in relation to another
    object body element. 
    This enables more flexibility when positioning multiple related elements
    on screen.
    """

    __position: tuple[int | float, int | float] # int: absolute offset         | float: relative offset to parent size
    __size: tuple[int | float, int | float] # int: absolute size / size offset | float: percentage sizing relative to relativeObj

    __relativeObjForPos: tuple[Optional[UIABCBody], Optional[UIABCBody]]
    __relativeObjPosRelationType: tuple[AlignmentType, AlignmentType]
    
    __relativeObjForSize: tuple[Optional[UIABCBody], Optional[UIABCBody]]


    def __init__(self, position: tuple[int | float, int | float], size: tuple[int | float, int | float],
                relativeObjectsForPosition: tuple[Optional[UIABCBody], Optional[UIABCBody]]=(None, None), 
                relativeObjectsForPositionRelationType: tuple[int, int]=(0, 0),
                relativeObjectsForSize: tuple[Optional[UIABCBody], Optional[UIABCBody]]=(None, None)) -> None:
        super().__init__(Rect()) # initialize empty Rect ~ 0,0,0,0

        self.__position = position
        self.__size = size
        self.__relativeObjForPos = relativeObjectsForPosition
        self.__relativeObjForSize = relativeObjectsForSize

        self.__relativeObjPosRelationType = (AlignmentType(relativeObjectsForPositionRelationType[0]), AlignmentType(relativeObjectsForPositionRelationType[1]))

        self.update()


    def _calculateSize(self) -> tuple[int, int]:
        """
        calculateSize calculates the size of the UIDynamicBody object.
        Two modes:
        1. Object is absolute sized: It just returns the absolute size of the object.
        2. Object is relative sized: 
            Size is calculated in respect to the parent UIBody(s) size(s).
            Given size is interpreted as either scale down of parent size (float)
            or offset of parent size (int).
        
        If relative positioned:
            Calls the `getSize` method(s) from parent UIBody('s)

        Returns:
            tuple[int, int] = (width, height) ~ the size of the UIDynamicBody object
        """
        absoluteSizeX: int = 0
        absoluteSizeY: int = 0
        selfSizeX: int | float
        selfSizeY: int | float
        (selfSizeX, selfSizeY) = self.__size

        #X-Size
        if self.__relativeObjForSize[0] is None:
            #absolute sized
            absoluteSizeX = int(selfSizeX)
        else:
            #relative sized
            relObjX: UIABCBody = self.__relativeObjForSize[0]

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
        if self.__relativeObjForSize[1] is None:
            #absolute sized
            absoluteSizeY = int(selfSizeY)
        else:
            #relative sized
            relObjY: UIABCBody = self.__relativeObjForSize[1]

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


    def _calculatePosition(self) -> tuple[int, int]:
        """
        calculatePosition calculates the position (top-left corner) of the UIDynamicBody object.
        Two modes:
        1. Object is absolute positioned: It just returns the absolute position of the object.
        2. Object is relative positioned: 
            Position is calculated in respect to the parent UIBody(s) position
            and the corner connection given by the relativeObjPosRelationType:
                child-corner -> parent-corner
                top-left to top-left (0,0)
                top-left to top-right (0,1)
                ...
                bottom-left to bottom-right (2,3)
                ...
                bottom-right to bottom-right (3,3)
            Furthermore the given 'position' is interpreted as offset. (if float relative to parent size)

        If relative positioned:
            Calls the `getSize` method from this UIBody
            Calls the `getPosition` method(s) from parent UIBody('s)
            Calls the `getSize` method(s) from parent UIBody('s)

        Returns:
            tuple[int, int] = (posX, posY) ~ the position of the top-left corner of the UIObject
        """
        absolutePosX: int = 0
        absolutePosY: int = 0
        selfPosX: int | float
        selfPosY: int | float
        (selfPosX, selfPosY) = self.__position

        #X-Position
        if self.__relativeObjForPos[0] is None:
            #absolute positioned
            absolutePosX = int(selfPosX)
        else:
            #relative positioned
            relObjX: UIABCBody = self.__relativeObjForPos[0]
            
            #interpret 'position' as offset
            if isinstance(selfPosX, int):
                absolutePosX += selfPosX
            else:
                #if float: relative to parent-size
                absolutePosX += int(selfPosX * relObjX.getSize()[0])
            
            #topleft: 0, topright: 1, bottomleft: 2, bottomright: 3
            absolutePosX += relObjX.getPosition()[0]
            connectionTypeChild: int = self.__relativeObjPosRelationType[0].value
            connectionTypeParent: int = self.__relativeObjPosRelationType[1].value
            connectionTypeLeftOrRightChild: int = connectionTypeChild % 2 # left: 0, right: 1
            connectionTypeLeftOrRightParent: int = connectionTypeParent % 2

            if connectionTypeLeftOrRightParent == 1:
                #use right edge of parent object
                absolutePosX += relObjX.getSize()[0]
            if connectionTypeLeftOrRightChild == 1:
                #use right edge of this object
                absolutePosX -= self.getSize()[0] # size should already be cached
        
        #Y-Position
        if self.__relativeObjForPos[1] is None:
            #absolute positioned
            absolutePosY = int(selfPosY)
        else:
            #relative positioned
            relObjY: UIABCBody = self.__relativeObjForPos[1]
            
            #interpret 'position' as offset
            if isinstance(selfPosY, int):
                absolutePosY += selfPosY
            else:
                #if float: relative to parent-size
                absolutePosY += int(selfPosY * relObjY.getSize()[1])
            
            #topleft: 0, topright: 1, bottomleft: 2, bottomright: 3
            absolutePosY += relObjY.getPosition()[1]
            connectionTypeChild: int = self.__relativeObjPosRelationType[0].value
            connectionTypeParent: int = self.__relativeObjPosRelationType[1].value
            connectionTypeTopOrBottomChild: int = connectionTypeChild // 2 # top: 0, bottom: 1
            connectionTypeTopOrBottomParent: int = connectionTypeParent // 2

            if connectionTypeTopOrBottomParent == 1:
                #use bottom edge of parent object
                absolutePosY += relObjY.getSize()[1]
            if connectionTypeTopOrBottomChild == 1:
                #use bottom edge of this object
                absolutePosY -= self.getSize()[1] # size should already be cached

        return (absolutePosX, absolutePosY)


    @override
    def update(self) -> None:
        """
        update calculates the position and size of the UIElementBody and
        caches the values in hte UIElementBody attributes.

        (override because in DynamicBody the calculatePosition function
            depends on the calculateSize -> suboptimal)
        """
        self._rect.setSize(self._calculateSize())
        self._rect.setPosition(self._calculatePosition())


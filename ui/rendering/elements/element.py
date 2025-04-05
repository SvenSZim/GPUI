from abc import ABC, abstractmethod
from typing import Generic, TypeVar, override

from ...utility           import Rect, iRect
from ..renderer           import Renderer
from ..createinfo         import CreateInfo
from .elementcore         import ElementCore
from .elementdata         import ElementData
from .elementcreateoption import ElementCreateOption
from .elementprefab       import ElementPrefab

Point = tuple[float, float]


ElementCls = TypeVar('ElementCls', bound='Element')

Core         = TypeVar('Core'        , bound=ElementCore        ) 
Data         = TypeVar('Data'        , bound=ElementData        )
CreateOption = TypeVar('CreateOption', bound=ElementCreateOption)
Prefab       = TypeVar('Prefab'      , bound=ElementPrefab      )

class Element(Generic[Core, Data, CreateOption, Prefab], Renderer, iRect, ABC):

    _core: Core         # refering UI-Element which gets rendered by the Renderer
    _renderData: Data   # needed data for rendering the element onto the screen

    # -------------------- creation --------------------

    def __init__(self, core: Core, renderData: Data, active: bool=True) -> None:
        super().__init__(active)
        self._core = core
        self._renderData = renderData

    @staticmethod
    @abstractmethod
    def fromCreateOptions(createOptions: list[CreateOption]) -> CreateInfo[ElementCls]:
        """
        fromCreateOptions creates the element from createoptions.

        Args:
            createoptions (list[CreateOption]): the list of create-options to be used for creating

        Returns (creator for this class): createinfo for this class
        """
        pass

    @staticmethod
    @abstractmethod
    def fromPrefab(prefab: Prefab) -> CreateInfo[ElementCls]:
        """
        fromPrefab creates the element from a prefab.

        Args:
            prefab (Prefab): the prefab to be created

        Returns (creator for this class): instance of the created element
        """
        pass

    # -------------------- iRect-implementation -------------------- 

    @override
    def getSize(self) -> tuple[int, int]:
        """
        getSize returns the size of the element.

        Returns (tuple[int, int]) ~ (width, height): size of the element
        """
        return self._core.getSize()

    @override
    def getPosition(self) -> tuple[int, int]:
        """
        getPosition return the position of the element.

        Returns (tuple[int, int]) ~ (x-pos, y-pos): position of the element
        """
        return self._core.getPosition()

    # -------------------- additional-getter --------------------

    def getRect(self) -> Rect:
        """
        getRect returns the position and size of the element stored in a Rect object

        Returns (Rect): Rect object containing the pos and size of the element
        """
        return self._core.getRect()

    def getCore(self) -> Core:
        """
        getCore returns the stored core of the element.
        (should only be used to align)

        Returns (Core): the stored core of the element
        """
        return self._core

    # -------------------- positional-setter --------------------
    
    def alignaxis(self, other: 'Element | Core | iRect', axis: int, offset: int=0, keepSize: bool=True) -> None:
        """
        alignaxis creates a LayoutRequest to align the axis of the core element with the given one.

        Args:
            other    (Element or Core or Rect)                   : the reference to align against
            axis     (int ~ 0: Left, 1: Right, 2: Top, 3: Bottom): the axis to align
            offset   (int)                                       : offset between the align
            keepSize (bool)                                      : boolean if the connection should keep the size
        """
        if isinstance(other, Element):
            other = other.getCore()
        self._core.alignaxis(other, axis, offset, keepSize)

    def alignpoint(self, other: 'Element | Core | iRect', myPoint: Point=(0.0,0.0), otherPoint: Point=(0.0,0.0), offset: int | tuple[int, int] = 0) -> None:
        """
        pointalign creates a LayoutRequest to align two relative points of elements fixed onto one another.

        Args:
            other:      (Element or Core or Rect)   : the reference to align against
            myPoint:    (Point)                     : the relative position on this element to align
            otherPoint: (Point)                     : the relative position on the other element to align against
        """
        if isinstance(other, Element):
            other = other.getCore()
        self._core.alignpoint(other, myPoint, otherPoint, offset=offset)

    def alignnextto(self, other: 'Element | Core | iRect', where: int, offset: int=0, keepSize: bool=True) -> None:
        """
        alignnextto creates a LayoutRequest to align the core element next to a reference object.

        Args:
            other    (Element or Core or Rect)                          : the reference to align against
            where    (int ~ 0: to the Left, 1: Right, 2: Top, 3: Bottom): the position where to place the core
            offset   (int)                                              : offset between the align
            keepSize (bool)                                             : boolean if the connection should keep the size
        """
        if isinstance(other, Element):
            other = other.getCore()
        self._core.alignnextto(other, where, offset, keepSize)

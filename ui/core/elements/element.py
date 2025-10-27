from abc import ABC, abstractmethod
from typing import Any, Generic, Optional, TypeVar, override
import xml.etree.ElementTree as ET

from ...utility           import Rect, iRect, Parsable, AlignType, StyledDefault
from ...interaction       import EventManager
from ..renderer           import Renderer
from ..style              import StyleManager
from .body                import Body
from .elementcore         import ElementCore
from .elementdata         import ElementData


ElementCls = TypeVar('ElementCls', bound='Element')

Core = TypeVar('Core', bound=ElementCore) 
Data = TypeVar('Data', bound=ElementData)

class Element(Generic[Core, Data], Renderer, Parsable, iRect, ABC):

    # -------------------- static --------------------

    styleTags: list[str] = ['style', 'styled', 'styleid', 'styledid']

    parserCallEvent: str = EventManager.createEvent()
    parserRequest: Optional[ET.Element] = None
    parserResponse: 'Optional[Element]' = None

    @staticmethod
    def updateLayout() -> None:
        EventManager.triggerEvent(Body.getLayoutUpdateEvent())

    @staticmethod
    def _validateType(value: Any, expected_type: type | tuple[type, ...], param_name: str) -> None:
        """Validate a parameter's type with descriptive error message.

        Args:
            value: Value to check
            expected_type: Type or tuple of types to validate against
            param_name: Parameter name for error message

        Raises:
            ValueError: If value is not of expected type(s)
        """
        if not isinstance(value, expected_type):
            type_names = (
                [t.__name__ for t in expected_type]
                if isinstance(expected_type, tuple)
                else [expected_type.__name__]
            )
            got_type = type(value).__name__
            raise ValueError(
                f'{param_name} must be {" or ".join(type_names)}, got {got_type}'
            )

    @staticmethod
    def getStyledElement(element: str | StyledDefault, stylename: Optional[str]=None) -> 'Optional[Element]':
        if stylename is None:
            stylename = StyleManager.defaultStyle
        Element.parserRequest = StyleManager.getStyledElementNode(str(element), stylename)
        EventManager.triggerEvent(Element.parserCallEvent)
        resp: Optional[Element] = Element.parserResponse
        Element.parserResponse = None
        return resp

    # -------------------- creation --------------------

    _layoutUpdateEvent: str = EventManager.createEvent()

    _core      : Core   # non-renderspecific data and functionality for the element
    _renderData: Data   # needed data for rendering the element onto the screen

    def __init__(self, core: Core, renderData: Data, active: bool=True) -> None:
        super().__init__(active)
        self._core = core
        self._renderData = renderData
        self.setZIndex(0) # set default z-index

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

    def getInnerSizing(self, elSize: tuple[int, int], args: dict[str, Any]={}) -> tuple[int, int]:
        return self._core.getInnerSizing(elSize, args)

    # -------------------- positional-setter --------------------
    
    def align(self, other: 'Element | Core | iRect', align: AlignType=AlignType.iTiL, alignX: bool=True, alignY: bool=True,
              offset: int | tuple[int, int]=0, keepSize: bool=True) -> None:
        """
        align creates a LayoutRequest to align the element with the given one.

        Args:
            other   (Element or Core or Rect)   : the reference to align against
            align   (Align)                     : the type of alignment to use
        """
        mybody: Body = self.getCore().getBody()
        if isinstance(other, Element):
            other = other.getCore().getBody()
        elif isinstance(other, ElementCore):
            other = other.getBody()
        
        if isinstance(offset, int):
            offset = (offset, offset)
        mybody.align(other, align, alignX=alignX, alignY=alignY, offset=offset, keepSize=keepSize)

    def alignSize(self, other: 'Element | Core | iRect', alignX: bool=True, alignY: bool=True,
                  relativeAlign: float | tuple[float, float]=1.0, absoluteOffset: int | tuple[int, int]=0) -> None:

        """
        alignSize creates a LayoutRequest to align the element-size with the given one.

        Args:
            other           (Element or Core or Rect)       : the reference to align against
            alignX          (bool=True)                     : if the width should be aligned
            alignY          (bool=True)                     : if the height should be aligned
            relativeAlign   (float or tuple[float, float]   : which proportion of the w/h should be used
            absoluteOffset  (int or tuple[int, int])        : which absolute offset of the w/h should be used
        """
        mybody: Body = self.getCore().getBody()
        if isinstance(other, Element):
            other = other.getCore().getBody()
        elif isinstance(other, ElementCore):
            other = other.getBody()
        
        if isinstance(relativeAlign, float):
            relativeAlign = (relativeAlign, relativeAlign)

        if isinstance(absoluteOffset, int):
            absoluteOffset = (absoluteOffset, absoluteOffset)

        if isinstance(relativeAlign, int):
            raise ValueError(
                'relativeAlign must be float or tuple of floats (0.0-1.0), '
                f'got int: {relativeAlign}'
            )

        mybody.addReferenceConnection(other, (alignX, alignY), (1.0, 1.0), relativeAlign, offset=absoluteOffset, fixedGlobal=(False, False), keepSize=(False, False))


    def alignpoint(self, other: 'Element | Core | iRect', myPoint: tuple[float, float]=(0.0,0.0),
                   otherPoint: tuple[float, float]=(0.0,0.0), offset: int | tuple[int, int] = 0, keepSize: bool=True) -> None:
        """
        alignpoint creates a LayoutRequest to align two relative points of elements fixed onto one another.

        Args:
            other:      (Element or Core or Rect)   : the reference to align against
            myPoint:    (tuple[float, float])       : the relative position on this element to align
            otherPoint: (Point)                     : the relative position on the other element to align against
            keepSize    (bool)                      : boolean if the connection should keep the size
        """
        mybody: Body = self.getCore().getBody()
        if isinstance(other, Element):
            other = other.getCore()
        if isinstance(other, ElementCore):
            other = other.getBody()

        if isinstance(offset, int):
            offset = (offset, offset)
        mybody.addReferenceConnection(other, (True, True), myPoint, otherPoint, offset=offset, keepSize=(keepSize, keepSize))

    def forceUpdate(self) -> None:
        self._core._body.forceUpdate()

    #-------------------- access-point --------------------

    def _set(self, args: dict[str, Any], sets: int=-1, maxDepth: int=-1, skips: bool=False) -> bool:
        applied: bool = False
        for tag, value in args.items():
            match tag.lower():
                case 'posx' | 'x':
                    applied = True
                    if not skips:
                        Element._validateType(value, int, 'posX')
                        self.align(Rect(topleft=(value,0)), alignY=False)
                case 'posy' | 'y':
                    applied = True
                    if not skips:
                        Element._validateType(value, int, 'posY')
                        self.align(Rect(topleft=(0,value)), alignX=False)
                case 'position' | 'pos':
                    applied = True
                    if not skips:
                        Element._validateType(value, tuple, 'position')
                        if len(value) != 2 or not all(isinstance(x, int) for x in value):
                            raise ValueError('position must be a tuple of 2 integers, got: ' + str(value))
                        self.align(Rect(topleft=value))
                case 'width':
                    applied = True
                    if not skips:
                        Element._validateType(value, int, 'width')
                        self.alignSize(Rect(size=(value,0)), alignY=False)
                case 'height':
                    applied = True
                    if not skips:
                        Element._validateType(value, int, 'height')
                        self.alignSize(Rect(size=(0,value)), alignX=False)
                case 'size':
                    applied = True
                    if not skips:
                        Element._validateType(value, tuple, 'size')
                        if len(value) != 2 or not all(isinstance(x, int) for x in value):
                            raise ValueError('size must be a tuple of 2 integers, got: ' + str(value))
                        self.alignSize(Rect(size=value))
        return applied

    @abstractmethod
    def set(self, args: dict[str, Any], sets: int=-1, maxDepth: int=-1, skips: list[int]=[0]) -> int:
        """
        set is a general access point to an element. It has some basic functionality implemented and is overridden
        by some elements for more specific behavior (updating text in Text, subscribing to buttonpresses in button, etc.).
        set also recursively applies the given args to all children until the given amount of
        'sets' or the maxDepth is reached. A 'set' is counted if any of the given args can be applied to the element.

        Args:
            args (dict[str, Any]): Arguments to be set
            sets (int)           : Amount of sets to be done (-1 -> no limit)
            maxDepth (int)       : Maximum depth to apply to (-1 -> no limit)
            skips (list[int])    : Indices or keys that should be skipped when applying args

        Returns (int): the amount of 'sets' applied
        """
        pass


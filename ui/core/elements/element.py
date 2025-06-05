from abc import ABC
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

    @staticmethod
    def updateLayout() -> None:
        EventManager.triggerEvent(Body.getLayoutUpdateEvent())

    parserCallEvent: str = EventManager.createEvent()
    parserRequest: Optional[ET.Element] = None
    parserResponse: 'Optional[Element]' = None

    @staticmethod
    def getStyledElement(element: str | StyledDefault, stylename: str) -> 'Optional[Element]':
        Element.parserRequest = StyleManager.getStyledElementNode(str(element), stylename)
        EventManager.triggerEvent(Element.parserCallEvent)
        resp: Optional[Element] = Element.parserResponse
        Element.parserResponse = None
        return resp

    @staticmethod
    def getDefaultElement(tag: StyledDefault) -> 'Optional[Element]':
        Element.parserRequest = StyleManager.getDefault(tag)
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
    
    def align(self, other: 'Element | Core | iRect', align: AlignType=AlignType.iTiL, ignoreX: bool=False, ignoreY: bool=False,
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
        mybody.align(other, align, ignoreX=ignoreX, ignoreY=ignoreY, offset=offset, keepSize=keepSize)

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
            raise ValueError('ELEMENT::RELATIVEALIGN IS INT ?!?!')

        mybody.addReferenceConnection(other, (alignX, alignY), (1.0, 1.0), relativeAlign, offset=absoluteOffset, fixedGlobal=(False, False), keepSize=(False, False))


    def alignpoint(self, other: 'Element | Core | iRect', myPoint: tuple[float, float]=(0.0,0.0), otherPoint: tuple[float, float]=(0.0,0.0), offset: int | tuple[int, int] = 0, keepSize: bool=True) -> None:
        """
        pointalign creates a LayoutRequest to align two relative points of elements fixed onto one another.

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

    def set(self, args: dict[str, Any], sets: int=-1, maxDepth: int=-1) -> int:
        """
        set is a general access point to an element. It has some basic functionality implemented and is overridden
        by some elements for more specific behavior (updating text in Text, subscribing to buttonpresses in button, etc.).
        set also recursivly applies the given args to all children until the given amount of
        'sets' or the maxDepth is reached. A 'set' is counted, if any of the given args can be applied to the element.

        Returns (int): the amount of 'sets' applied
        """
        s: int = 0
        for tag, value in args.items():
            match tag:
                case 'posX':
                    s = 1
                    if isinstance(value, int):
                        self.align(Rect(topleft=(value,0)), ignoreY=True)
                    else:
                        raise ValueError('posX expects an int')
                case 'posY':
                    s = 1
                    if isinstance(value, int):
                        self.align(Rect(topleft=(0,value)), ignoreX=True)
                    else:
                        raise ValueError('posX expects an int')
                case 'position':
                    s = 1
                    if isinstance(value, tuple):
                        self.align(Rect(topleft=value))
                    else:
                        raise ValueError('position expects an 2-tuple of ints')
        return s


from typing import Any, Optional, override
from math import sqrt

from .....utility import Rect, Color
from .....display import Surface
from .....interaction import EventManager

from ...body    import Body
from ..atom             import Atom
from .linecore          import LineCore
from .linedata          import LineData, AltMode

class Line(Atom[LineCore, LineData]):
    """
    Line is a simple ui-atom-element for drawing a line.
    """

    # -------------------- creation --------------------

    def __init__(self, rect: Rect, renderData: LineData, active: bool=True) -> None:
        super().__init__(LineCore(rect), renderData, active)
        
        self.__renderCache = []
        EventManager.quickSubscribe(Body.getLayoutUpdateEvent(), self.updateRenderData)

    @override
    def copy(self) -> 'Line':
        return Line(Rect(), renderData=self._renderData.copy(), active=self.isActive())

    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'Line':
        return Line(Rect(), renderData=LineData.parseFromArgs(args))

    # -------------------- rendering --------------------

    __renderCache: list[tuple[Rect | tuple[tuple[int, int], tuple[int, int], int], Color]]

    @override
    def updateRenderData(self) -> None:
        self.__renderCache = []

        #calculate render borderbox
        rect: Rect = self.getRect()

        #check for errors in boxsize
        if rect.isZero():
            return
        if rect.width < 0:
            rect = Rect((rect.left + rect.width, rect.top), (-rect.width, rect.height))
        if rect.height < 0:
            rect = Rect((rect.left, rect.top + rect.height), (rect.width, -rect.height))
        
        #apply partialInset
        def applyPartial(rect: Rect, partialInset: tuple[float, float] | float | tuple[int, int] | int) -> Rect:
            if isinstance(partialInset, tuple):
                if isinstance(partialInset[0], float):
                    return Rect((rect.left + int(rect.width * partialInset[0]),
                                 rect.top + int(rect.height * partialInset[1])),
                                (int(rect.width * (1.0 - 2 * partialInset[0])), int(rect.height * (1.0 - 2 * partialInset[1]))))
                else:
                    assert isinstance(partialInset[1], int)
                    insetX = min(partialInset[0], int(rect.width*0.5))
                    insetY = min(partialInset[1], int(rect.height*0.5))
                    return Rect((rect.left + insetX, rect.top + insetY), (rect.width - 2 * insetX, rect.height - 2 * insetY))
            else:
                return applyPartial(rect, (partialInset, partialInset))
        
        globalInset: tuple[float, float] | float | tuple[int, int] | int = self._renderData.inset
        rect = applyPartial(rect, globalInset)
            
        sectionOrder: list[str] = self._renderData.order
        if len(sectionOrder) == 0:
            sectionOrder = ['']

        orderIndex: int = 0

        JIGGLE: int = max(1, int(0.003 * max(rect.width, rect.height)))
        whratio: float = rect.width/rect.height if rect.height > 0 else 1
        absNormalizer: float = 1/sqrt(1 + whratio*whratio) if rect.height > 0 and rect.width > 0 else 1

        nextStep: int | float = self._renderData.sizes[sectionOrder[orderIndex]] if sectionOrder[orderIndex] in self._renderData.sizes else self._renderData.sizes['']
        stepSizeX: float
        stepSizeY: float
        if isinstance(nextStep, float):
            stepSizeX = rect.width*nextStep
            stepSizeY = rect.height*nextStep
        else:
            stepSizeX = nextStep*whratio*absNormalizer if rect.width > 0 else 0
            stepSizeY = nextStep*absNormalizer if rect.height > 0 else 0

        cline: list[float] = [float(x) for x in rect.getPosition()]
        color: Optional[Color]
        thickness: int
        altmode: AltMode
        while rect.collidepoint((int(cline[0] + stepSizeX), int(cline[1] + stepSizeY))):
            color = self._renderData.colors[sectionOrder[orderIndex]] if sectionOrder[orderIndex] in self._renderData.colors else self._renderData.colors['']
            thickness = self._renderData.thickness[sectionOrder[orderIndex]] if sectionOrder[orderIndex] in self._renderData.thickness else self._renderData.thickness['']
            altmode = self._renderData.altmode[sectionOrder[orderIndex]] if sectionOrder[orderIndex] in self._renderData.altmode else self._renderData.altmode['']
            match altmode:
                case AltMode.CROSS:
                    if color is not None:
                        if rect.width > JIGGLE and rect.height > JIGGLE:
                            if self._renderData.flip:
                                self.__renderCache.append((((int(cline[0]), rect.bottom + rect.top - int(cline[1])), (int(cline[0] + stepSizeX), rect.bottom + rect.top - int(cline[1] + stepSizeY)), thickness), color))
                                self.__renderCache.append((((int(cline[0]), rect.bottom + rect.top - int(cline[1] + stepSizeY)), (int(cline[0] + stepSizeX), rect.bottom + rect.top - int(cline[1])), thickness), color))
                            else:
                                self.__renderCache.append((((int(cline[0]), int(cline[1])), (int(cline[0] + stepSizeX), int(cline[1] + stepSizeY)), thickness), color))
                                self.__renderCache.append((((int(cline[0]), int(cline[1] + stepSizeY)), (int(cline[0] + stepSizeX), int(cline[1])), thickness), color))
                        else:
                            if rect.width > JIGGLE:
                                pJIGGLE = JIGGLE - rect.height
                                if self._renderData.flip:
                                    self.__renderCache.append((((int(cline[0]), rect.bottom + rect.top - int(cline[1])             + pJIGGLE), (int(cline[0] + stepSizeX), rect.bottom + rect.top - int(cline[1] + stepSizeY) - pJIGGLE), thickness), color))
                                    self.__renderCache.append((((int(cline[0]), rect.bottom + rect.top - int(cline[1] + stepSizeY) - pJIGGLE), (int(cline[0] + stepSizeX), rect.bottom + rect.top - int(cline[1])             + pJIGGLE), thickness), color))
                                else:
                                    self.__renderCache.append((((int(cline[0]), int(cline[1])             + pJIGGLE), (int(cline[0] + stepSizeX), int(cline[1] + stepSizeY) - pJIGGLE), thickness), color))
                                    self.__renderCache.append((((int(cline[0]), int(cline[1] + stepSizeY) - pJIGGLE), (int(cline[0] + stepSizeX), int(cline[1])             + pJIGGLE), thickness), color))
                            elif rect.height > JIGGLE:
                                pJIGGLE = JIGGLE - rect.width
                                if self._renderData.flip:
                                    self.__renderCache.append((((int(cline[0]) - pJIGGLE, rect.bottom + rect.top - int(cline[1])), (int(cline[0] + stepSizeX) + pJIGGLE, rect.bottom + rect.top - int(cline[1] + stepSizeY)), thickness), color))
                                    self.__renderCache.append((((int(cline[0]) - pJIGGLE, rect.bottom + rect.top - int(cline[1] + stepSizeY)), (int(cline[0] + stepSizeX) + pJIGGLE, rect.bottom + rect.top - int(cline[1])), thickness), color))
                                else:
                                    self.__renderCache.append((((int(cline[0]) - pJIGGLE, int(cline[1])), (int(cline[0] + stepSizeX) + pJIGGLE, int(cline[1] + stepSizeY)), thickness), color))
                                    self.__renderCache.append((((int(cline[0]) - pJIGGLE, int(cline[1] + stepSizeY)), (int(cline[0] + stepSizeX) + pJIGGLE, int(cline[1])), thickness), color))
                            else:
                                if self._renderData.flip:
                                    self.__renderCache.append((((int(cline[0]), rect.bottom + rect.top - int(cline[1])), (int(cline[0] + stepSizeX), rect.bottom + rect.top - int(cline[1] + stepSizeY)), thickness), color))
                                else:
                                    self.__renderCache.append((((int(cline[0]), int(cline[1])), (int(cline[0] + stepSizeX), int(cline[1] + stepSizeY)), thickness), color))
                case _:
                    if color is not None:
                        if self._renderData.flip:
                            self.__renderCache.append((((int(cline[0]), rect.bottom + rect.top - int(cline[1])), (int(cline[0] + stepSizeX), rect.bottom + rect.top - int(cline[1] + stepSizeY)), thickness), color))
                        else:
                            self.__renderCache.append((((int(cline[0]), int(cline[1])), (int(cline[0] + stepSizeX), int(cline[1] + stepSizeY)), thickness), color))
            cline[0] += stepSizeX
            cline[1] += stepSizeY
            orderIndex = (orderIndex + 1) % len(sectionOrder)
            nextStep = self._renderData.sizes[sectionOrder[orderIndex]] if sectionOrder[orderIndex] in self._renderData.sizes else self._renderData.sizes['']
            stepSizeX: float
            stepSizeY: float
            if isinstance(nextStep, float):
                stepSizeX = rect.width*nextStep
                stepSizeY = rect.height*nextStep
            else:
                stepSizeX = nextStep*whratio*absNormalizer if rect.width > 0 else 0
                stepSizeY = nextStep*absNormalizer if rect.height > 0 else 0

        color = self._renderData.colors[sectionOrder[orderIndex]] if sectionOrder[orderIndex] in self._renderData.colors else self._renderData.colors['']
        thickness = self._renderData.thickness[sectionOrder[orderIndex]] if sectionOrder[orderIndex] in self._renderData.thickness else self._renderData.thickness['']
        altmode = self._renderData.altmode[sectionOrder[orderIndex]] if sectionOrder[orderIndex] in self._renderData.altmode else self._renderData.altmode['']
        match altmode:
            case AltMode.CROSS:
                if color is not None:
                    if rect.width > JIGGLE and rect.height > JIGGLE:
                        if self._renderData.flip:
                            self.__renderCache.append((((int(cline[0]), rect.bottom + rect.top - int(cline[1])), (rect.right, rect.top), thickness), color))
                            self.__renderCache.append((((int(cline[0]), rect.top), (rect.right, rect.bottom + rect.top - int(cline[1])), thickness), color))
                        else:
                            self.__renderCache.append((((int(cline[0]), int(cline[1])), (rect.right, rect.bottom), thickness), color))
                            self.__renderCache.append((((int(cline[0]), rect.bottom), (rect.right, int(cline[1])), thickness), color))
                    elif rect.width > JIGGLE:
                        pJIGGLE = JIGGLE - rect.height
                        if self._renderData.flip:
                            self.__renderCache.append((((int(cline[0]), rect.bottom + rect.top - int(cline[1]) + pJIGGLE), (rect.right, rect.top - pJIGGLE), thickness), color))
                            self.__renderCache.append((((int(cline[0]), rect.top - pJIGGLE), (rect.right, rect.bottom + rect.top - int(cline[1]) + pJIGGLE), thickness), color))
                        else:
                            self.__renderCache.append((((int(cline[0]), int(cline[1]) + pJIGGLE), (rect.right, rect.bottom - pJIGGLE), thickness), color))
                            self.__renderCache.append((((int(cline[0]), rect.bottom - pJIGGLE), (rect.right, int(cline[1]) + pJIGGLE), thickness), color))
                    elif rect.height > JIGGLE:
                        pJIGGLE = JIGGLE - rect.width
                        if self._renderData.flip:
                            self.__renderCache.append((((int(cline[0]) - pJIGGLE, rect.bottom + rect.top - int(cline[1])), (rect.right + pJIGGLE, rect.top), thickness), color))
                            self.__renderCache.append((((int(cline[0]) - pJIGGLE, rect.top), (rect.right + pJIGGLE, rect.bottom + rect.top - int(cline[1])), thickness), color))
                        else:
                            self.__renderCache.append((((int(cline[0]) - pJIGGLE, int(cline[1])), (rect.right + pJIGGLE, rect.bottom), thickness), color))
                            self.__renderCache.append((((int(cline[0]) - pJIGGLE, rect.bottom), (rect.right + pJIGGLE, int(cline[1])), thickness), color))
                    else:
                        if self._renderData.flip:
                            self.__renderCache.append((((int(cline[0]), rect.bottom + rect.top - int(cline[1])), (rect.right, rect.top), thickness), color))
                        else:
                            self.__renderCache.append((((int(cline[0]), int(cline[1])), (rect.right, rect.bottom), thickness), color))
            case _:
                if color is not None:
                    if self._renderData.flip:
                        self.__renderCache.append((((int(cline[0]), rect.bottom + rect.top - int(cline[1])), (rect.right, rect.top), thickness), color))
                    else:
                        self.__renderCache.append((((int(cline[0]), int(cline[1])), (rect.right, rect.bottom), thickness), color))

    @override
    def render(self, surface: Surface) -> None:
        """
        render renders the Line onto the given surface

        Args:
            surface (Surface): the surface the Line should be drawn on
        """
        assert self._drawer is not None

        if self._active:
            for ob, color in self.__renderCache:
                if isinstance(ob, Rect):
                    self._drawer.drawrect(surface, ob, color)
                elif isinstance(ob, tuple):
                    self._drawer.drawline(surface, ob[0], ob[1], color, thickness=ob[2])


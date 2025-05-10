from typing import Any, Optional, override

from .....utility import Rect, Color
from .....display import Surface
from .....interaction import EventManager

from ...body           import Body
from ..atom            import Atom
from .boxcore          import BoxCore
from .boxdata          import BoxData, AltMode
from .boxcreateoption  import BoxCO
from .boxprefab        import BoxPrefab

class Box(Atom[BoxCore, BoxData, BoxCO, BoxPrefab]):
    """
    Box is a simple ui-atom-element for drawing a box.
    """

    # -------------------- creation --------------------

    def __init__(self, rect: Rect, renderData: BoxPrefab | list[BoxCO] | BoxData=BoxPrefab.BASIC, active: bool=True) -> None:
        assert self._renderstyle is not None

        if isinstance(renderData, list):
            myData: BoxData = BoxData()
            for createOption in renderData:
                myData += (createOption, self._renderstyle)
            renderData = myData
        elif isinstance(renderData, BoxPrefab):
            renderData = BoxData() * (renderData, self._renderstyle)

        assert isinstance(renderData, BoxData)
        super().__init__(BoxCore(rect), renderData, active)

        self.__renderCache = []
        EventManager.quickSubscribe(Body.getLayoutUpdateEvent(), self.updateRenderData)

    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'Box':
        data: BoxData = BoxData()
        for arg, v in args.items():
            if arg not in {'partitioning'}:
                values = v.split(';')
                labelValuePairs: list[str | tuple[str, str]] = [vv.split(':') for vv in values]
                for vv in labelValuePairs:
                    label: str
                    value: str
                    if len(vv) == 1:
                        label = ''
                        value = vv[0]
                    else:
                        label = Box.parseLabel(vv[0])
                        value = vv[1]
                    match arg:
                        case 'partial':
                            data.partialInset[label] = Box.parsePartial(value)
                        case 'color':
                            data.mainColor[label] = Box.parseColor(value)
                        case 'fillmode':
                            match value:
                                case 'checkerboard' | 'cb':
                                    data.altMode[label] = AltMode.CHECKERBOARD
                        case 'fillsize':
                            match value:
                                case 's':
                                    data.altLen[label] = 10
                                case 'l':
                                    data.altLen[label] = 20
                                case _:
                                    data.altLen[label] = int(value)
            else:
                match arg:
                    case 'partitioning':
                        data.partitioning = Box.parsePartition(v)
        return Box(Rect(), renderData=data)

    # -------------------- rendering --------------------

    __renderCache: list[tuple[Rect, Color]]

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
                    rect = Rect((rect.left + int(rect.width * (1.0 - partialInset[0])),
                                 rect.top + int(rect.height * (1.0 - partialInset[1]))),
                                (int(rect.width * (1.0 - 2 * partialInset[0])), int(rect.height * (1.0 - 2 * partialInset[1]))))
                else:
                    assert isinstance(partialInset[1], int)
                    rect = Rect((rect.left + partialInset[0], rect.top + partialInset[1]), (rect.width - 2 * partialInset[0], rect.height - 2 * partialInset[1]))
            elif isinstance(partialInset, float):
                inset: int = int(min(rect.width, rect.height) * partialInset)
                rect = Rect((rect.left + inset, rect.top + inset),
                            (rect.width - 2 * inset, rect.height - 2 * inset))
            else:
                rect = Rect((rect.left + partialInset, rect.top + partialInset), (rect.width - 2 * partialInset, rect.height - 2 * partialInset))
            return rect
        
        globalInset: tuple[float, float] | float | tuple[int, int] | int = self._renderData.partialInset['']
        rect = applyPartial(rect, globalInset)

        #apply partitioning
        partitionSizeX, partitionSizeY, partitionLabels = self._renderData.partitioning
        partitionSize: tuple[float, float] = (rect.width / partitionSizeX, rect.height / partitionSizeY)
        iPartitionSize: tuple[int, int] = (int(rect.width / partitionSizeX), int(rect.height / partitionSizeY))
        for ypartitionindex in range(partitionSizeY):
            for xpartitionindex in range(partitionSizeX):
                label: str = partitionLabels[partitionSizeX * ypartitionindex + xpartitionindex]

                partitionRect: Rect = Rect((int(rect.left + xpartitionindex * partitionSize[0]), int(rect.top + ypartitionindex * partitionSize[1])), iPartitionSize)
                partitionpartialInset: tuple[float, float] | float | tuple[int, int] | int = self._renderData.partialInset[label] if label != '' and label in self._renderData.partialInset else 0.0
                partitionRect = applyPartial(partitionRect, partitionpartialInset)

                color: Optional[Color] = self._renderData.mainColor[label] if label in self._renderData.mainColor else self._renderData.mainColor['']
                altmode: Optional[AltMode] = self._renderData.altMode[label] if label in self._renderData.altMode else self._renderData.altMode['']
                altcolor: Optional[Color] = self._renderData.altColor[label] if label in self._renderData.altColor else self._renderData.altColor['']
                altsize: float | int = self._renderData.altLen[label] if label in self._renderData.altLen else self._renderData.altLen['']

                #apply altmodes
                match altmode:
                    case AltMode.CHECKERBOARD:
                        if isinstance(altsize, float):
                            altsize = int(altsize * min(partitionRect.width, partitionRect.height))
                        start_rect: Rect = Rect(partitionRect.getPosition(), (altsize, altsize))
                        rowStartFirstColor: bool = True
                        while start_rect.bottom < partitionRect.bottom:
                            firstColor: bool = rowStartFirstColor
                            while start_rect.right < partitionRect.right:
                                if firstColor:
                                    if color is not None:
                                        self.__renderCache.append((start_rect, color))
                                else:
                                    if altcolor is not None:
                                        self.__renderCache.append((start_rect, altcolor))
                                firstColor = not firstColor
                                start_rect = Rect((start_rect.right, start_rect.top), (altsize, altsize))
                            if firstColor:
                                if color is not None:
                                    self.__renderCache.append((Rect((start_rect.left, start_rect.top), (partitionRect.right - start_rect.left, altsize)), color))
                            else:
                                if altcolor is not None:
                                    self.__renderCache.append((Rect((start_rect.left, start_rect.top), (partitionRect.right - start_rect.left, altsize)), altcolor))
                            rowStartFirstColor = not rowStartFirstColor
                            start_rect = Rect((partitionRect.left, start_rect.bottom), (altsize, altsize))
                        missing_height: int = partitionRect.bottom - start_rect.top
                        start_rect = Rect(start_rect.getPosition(), (altsize, missing_height))
                        while start_rect.right < partitionRect.right:
                            if rowStartFirstColor:
                                if color is not None:
                                    self.__renderCache.append((start_rect, color))
                            else:
                                if altcolor is not None:
                                    self.__renderCache.append((start_rect, altcolor))
                            rowStartFirstColor = not rowStartFirstColor
                            start_rect = Rect((start_rect.right, start_rect.top), (altsize, missing_height))
                        if rowStartFirstColor:
                            if color is not None:
                                self.__renderCache.append((Rect((start_rect.left, start_rect.top), (partitionRect.right - start_rect.left, missing_height)), color))
                        else:
                            if altcolor is not None:
                                self.__renderCache.append((Rect((start_rect.left, start_rect.top), (partitionRect.right - start_rect.left, missing_height)), altcolor))

                    case _:
                        if color is not None:
                            self.__renderCache.append((partitionRect, color))



    @override
    def render(self, surface: Surface) -> None:
        """
        render renders the Box onto the given surface

        Args:
            surface: Surface = the surface the Box should be drawn on
        """
        assert self._drawer is not None
        
        if self._active:
            for rect, color in self.__renderCache:
                self._drawer.drawrect(surface, rect, color)

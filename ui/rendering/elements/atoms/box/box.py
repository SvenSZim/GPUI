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
            if arg not in ['partitioning']:
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
                        case 'inset':
                            data.partialInset[label] = Box.parsePartial(value)
                        case 'colors':
                            data.colors[label] = Box.parseColor(value)
                        case 'fillmode':
                            match value:
                                case 'checkerboard' | 'cb':
                                    data.altMode[label] = AltMode.CHECKERBOARD
                                case 'striped_vert' | 'strv':
                                    data.altMode[label] = AltMode.STRIPED_V
                                case 'striped_hor' | 'strh':
                                    data.altMode[label] = AltMode.STRIPED_H
                        case 'fillsize':
                            match value:
                                case 's':
                                    data.altLen[label] = 10
                                case 'l':
                                    data.altLen[label] = 20
                                case _:
                                    if '.' in value:
                                        vk, nk = [Box.extractNum(vvv) for vvv in value.split('.')][:2]
                                        data.altLen[label] = int(vk) + int(nk) / 10**len(nk)
                                    else:
                                        data.altLen[label] = int(Box.extractNum(value))
                        case 'sectionorders':
                            data.orders[label] = Box.parseList(value)
            else:
                match arg:
                    case 'partitioning':
                        data.partitioning = Box.parsePartition(v)
        return Box(Rect(), renderData=data)

    # -------------------- rendering --------------------

    __renderCache: list[tuple[Rect | tuple[tuple[int, int], tuple[int, int], int], Color]]

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

                order: list[str] = self._renderData.orders[label] if label in self._renderData.orders else self._renderData.orders['']
                if len(order) == 0:
                    order = ['']
                altmode: AltMode = self._renderData.altMode[label] if label in self._renderData.altMode else self._renderData.altMode['']
                altsize: float | int = self._renderData.altLen[label] if label in self._renderData.altLen else self._renderData.altLen['']
                color: Optional[Color] = self._renderData.colors[order[0]] if order[0] in self._renderData.colors else self._renderData.colors['']

                #apply altmodes
                match altmode:
                    case AltMode.CHECKERBOARD:
                        rowStartFirstColor: int = 0
                        firstColor: int = rowStartFirstColor
                        if isinstance(altsize, float):
                            altsize = altsize * min(partitionRect.width, partitionRect.height)
                        top: float = partitionRect.top
                        tile: Rect
                        while top + altsize < partitionRect.bottom:
                            firstColor = rowStartFirstColor
                            left: float = partitionRect.left
                            while left + altsize < partitionRect.right:
                                color = self._renderData.colors[order[firstColor]] if order[firstColor] in  self._renderData.colors else self._renderData.colors['']
                                tile = Rect((int(left), int(top)), (int(altsize), int(altsize)))
                                if color is not None:
                                    self.__renderCache.append((tile, color))
                                firstColor = (firstColor + 1) % len(order)
                                left += altsize
                            tile = Rect((int(left), int(top)), (partitionRect.right - int(left), int(altsize)))
                            color = self._renderData.colors[order[firstColor]] if order[firstColor] in  self._renderData.colors else self._renderData.colors['']
                            if color is not None:
                                self.__renderCache.append((tile, color))
                            rowStartFirstColor = (rowStartFirstColor + 1) % len(order)
                            top += altsize
                        missing_height: int = partitionRect.bottom - int(top)
                        left: float = partitionRect.left
                        while left + altsize < partitionRect.right:
                            color = self._renderData.colors[order[rowStartFirstColor]] if order[rowStartFirstColor] in  self._renderData.colors else self._renderData.colors['']
                            tile = Rect((int(left), int(top)), (int(altsize), missing_height))
                            if color is not None:
                                self.__renderCache.append((tile, color))
                            rowStartFirstColor = (rowStartFirstColor + 1) % len(order)
                            left += altsize
                        color = self._renderData.colors[order[rowStartFirstColor]] if order[rowStartFirstColor] in  self._renderData.colors else self._renderData.colors['']
                        if color is not None:
                            self.__renderCache.append((Rect((int(left), int(top)), (partitionRect.right - int(left), missing_height)), color))

                    case AltMode.STRIPED_V:
                        if isinstance(altsize, float):
                            altsize = altsize * partitionRect.width
                        firstColor: int = 0
                        left: float = partitionRect.left
                        while left + altsize < partitionRect.right:
                            color = self._renderData.colors[order[firstColor]] if order[firstColor] in  self._renderData.colors else self._renderData.colors['']
                            stripe: Rect = Rect((int(left), partitionRect.top), (int(altsize), partitionRect.height))
                            if color is not None:
                                self.__renderCache.append((stripe, color))
                            firstColor = (firstColor + 1) % len(order)
                            left += altsize
                        color = self._renderData.colors[order[firstColor]] if order[firstColor] in  self._renderData.colors else self._renderData.colors['']
                        if color is not None:
                            self.__renderCache.append((Rect((int(left), partitionRect.top), (partitionRect.right - int(left), partitionRect.height)), color))

                    case AltMode.STRIPED_H:
                        if isinstance(altsize, float):
                            altsize = altsize * partitionRect.height
                        firstColor: int = 0
                        top: float = partitionRect.top
                        while top + altsize < partitionRect.bottom:
                            color = self._renderData.colors[order[firstColor]] if order[firstColor] in  self._renderData.colors else self._renderData.colors['']
                            stripe: Rect = Rect((partitionRect.left, int(top)), (partitionRect.width, int(altsize)))
                            if color is not None:
                                self.__renderCache.append((stripe, color))
                            firstColor = (firstColor + 1) % len(order)
                            top += altsize
                        color = self._renderData.colors[order[firstColor]] if order[firstColor] in  self._renderData.colors else self._renderData.colors['']
                        if color is not None:
                            self.__renderCache.append((Rect((partitionRect.left, int(top)), (partitionRect.width, partitionRect.bottom - int(top))), color))

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
            for ob, color in self.__renderCache:
                if isinstance(ob, Rect):
                    self._drawer.drawrect(surface, ob, color)
                elif isinstance(ob, tuple):
                    self._drawer.drawline(surface, ob[0], ob[1], color, thickness=ob[2])

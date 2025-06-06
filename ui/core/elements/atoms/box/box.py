from typing import Any, Optional, override

from .....utility import Rect, Color
from .....display import Surface
from .....interaction import EventManager

from ...body           import Body
from ..atom            import Atom
from .boxcore          import BoxCore
from .boxdata          import BoxData, AltMode, Filters

filtertype = Filters | tuple[Filters, tuple[float, float, tuple[float, float]], bool]

class Box(Atom[BoxCore, BoxData]):
    """
    Box is a simple ui-atom-element for drawing a box.
    """

    # -------------------- creation --------------------

    def __init__(self, renderData: BoxData, active: bool=True) -> None:
        super().__init__(BoxCore(), renderData, active)

        self.__renderCache = []
        EventManager.quickSubscribe(Body.getLayoutUpdateEvent(), self.updateRenderData)

    @override
    def copy(self) -> 'Box':
        return Box(renderData=self._renderData.copy(), active=self.isActive())

    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'Box':
        return Box(renderData=BoxData.parseFromArgs(args))

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
        
        globalInset: tuple[float, float] | float | tuple[int, int] | int = self._renderData.partialInset['']
        rect = applyPartial(rect, globalInset)

        #apply filters
        USE_POINT_TO_CHECK_FILTER = (0.5, 0.5)
        def isInsideFilter(rect: Rect, filt: filtertype, point: tuple[int, int]):
            if not isinstance(filt, tuple):
                return True
            match filt[0]:
                case Filters.LINEAR:
                    x, y, d = filt[1]
                    xx, yy = rect.getPoint((x, y))
                    dd: float
                    if d[0] > 0.0 and d[1] > 0.0:
                        dd = max(d[0] * rect.width, d[1] * rect.height)
                    else:
                        dd = d[0] * rect.width + d[1] * rect.height
                    if filt[2]:
                        return abs(point[0] - xx) + abs(point[1] - yy) >= dd
                    else:
                        return abs(point[0] - xx) + abs(point[1] - yy) <= dd
                case Filters.QUADRATIC:
                    x, y, d = filt[1]
                    xx, yy = rect.getPoint((x, y))
                    dd: float
                    if d[0] > 0.0 and d[1] > 0.0:
                        dd = max(d[0] * rect.width, d[1] * rect.height)
                    else:
                        dd = d[0] * rect.width + d[1] * rect.height
                    if filt[2]:
                        return (point[0] - xx)**2 + (point[1] - yy)**2 >= dd**2
                    else:
                        return (point[0] - xx)**2 + (point[1] - yy)**2 <= dd**2
            return False

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

                order: list[str] = self._renderData.orders[label] if label in self._renderData.orders else []
                if len(order) == 0:
                    order = ['asiujdbfnoiasdjf']
                altmode: AltMode = self._renderData.altMode[label] if label in self._renderData.altMode else self._renderData.altMode['']
                altsize: float | int = self._renderData.altLen[label] if label in self._renderData.altLen else self._renderData.altLen['']
                partitionColor: Optional[Color] = self._renderData.colors[label] if label in self._renderData.colors else self._renderData.colors['']
                partitionFilter: filtertype = self._renderData.filters[label] if label in self._renderData.filters else self._renderData.filters['']
                
                color: Optional[Color] = self._renderData.colors[order[0]] if order[0] in self._renderData.colors else partitionColor
                filter: filtertype = self._renderData.filters[order[0]] if order[0] in self._renderData.filters else partitionFilter

                if isinstance(altsize, float):
                    altsize = altsize * min(partitionRect.width, partitionRect.height)
                rowStartOrderIndex: int = 0
                orderIndex: int = rowStartOrderIndex
                top: float = partitionRect.top
                tile: Rect
                #apply altmodes
                match altmode:
                    case AltMode.CHECKERBOARD:
                        while top + altsize < partitionRect.bottom:
                            orderIndex = rowStartOrderIndex
                            left: float = partitionRect.left
                            while left + altsize < partitionRect.right:
                                color = self._renderData.colors[order[orderIndex]] if order[orderIndex] in self._renderData.colors else partitionColor
                                filter = self._renderData.filters[order[orderIndex]] if order[orderIndex] in self._renderData.filters else partitionFilter
                                tile = Rect((int(left), int(top)), (int(altsize), int(altsize)))
                                if color is not None and isInsideFilter(partitionRect, filter, tile.getPoint(USE_POINT_TO_CHECK_FILTER)):
                                    self.__renderCache.append((tile, color))
                                orderIndex = (orderIndex + 1) % len(order)
                                left += altsize
                            color = self._renderData.colors[order[orderIndex]] if order[orderIndex] in  self._renderData.colors else partitionColor
                            filter = self._renderData.filters[order[orderIndex]] if order[orderIndex] in self._renderData.filters else partitionFilter
                            tile = Rect((int(left), int(top)), (partitionRect.right - int(left), int(altsize)))
                            if color is not None and isInsideFilter(partitionRect, filter, tile.getPoint(USE_POINT_TO_CHECK_FILTER)):
                                self.__renderCache.append((tile, color))
                            rowStartOrderIndex = (rowStartOrderIndex + 1) % len(order)
                            top += altsize
                        missing_height: int = partitionRect.bottom - int(top)
                        left: float = partitionRect.left
                        while left + altsize < partitionRect.right:
                            color = self._renderData.colors[order[rowStartOrderIndex]] if order[rowStartOrderIndex] in  self._renderData.colors else partitionColor
                            filter = self._renderData.filters[order[rowStartOrderIndex]] if order[rowStartOrderIndex] in self._renderData.filters else partitionFilter
                            tile = Rect((int(left), int(top)), (int(altsize), missing_height))
                            if color is not None and isInsideFilter(partitionRect, filter, tile.getPoint(USE_POINT_TO_CHECK_FILTER)):
                                self.__renderCache.append((tile, color))
                            rowStartOrderIndex = (rowStartOrderIndex + 1) % len(order)
                            left += altsize
                        color = self._renderData.colors[order[rowStartOrderIndex]] if order[rowStartOrderIndex] in  self._renderData.colors else partitionColor
                        filter = self._renderData.filters[order[rowStartOrderIndex]] if order[rowStartOrderIndex] in self._renderData.filters else partitionFilter
                        tile = Rect((int(left), int(top)), (partitionRect.right - int(left), missing_height))
                        if color is not None and isInsideFilter(partitionRect, filter, tile.getPoint(USE_POINT_TO_CHECK_FILTER)):
                            self.__renderCache.append((tile, color))

                    case AltMode.STRIPED_V:
                        while top + altsize < partitionRect.bottom:
                            orderIndex = rowStartOrderIndex
                            left: float = partitionRect.left
                            while left + altsize < partitionRect.right:
                                color = self._renderData.colors[order[orderIndex]] if order[orderIndex] in self._renderData.colors else partitionColor
                                filter = self._renderData.filters[order[orderIndex]] if order[orderIndex] in self._renderData.filters else partitionFilter
                                tile = Rect((int(left), int(top)), (int(altsize), int(altsize)))
                                if color is not None and isInsideFilter(partitionRect, filter, tile.getPoint(USE_POINT_TO_CHECK_FILTER)):
                                    self.__renderCache.append((tile, color))
                                orderIndex = (orderIndex + 1) % len(order)
                                left += altsize
                            color = self._renderData.colors[order[orderIndex]] if order[orderIndex] in  self._renderData.colors else partitionColor
                            filter = self._renderData.filters[order[orderIndex]] if order[orderIndex] in self._renderData.filters else partitionFilter
                            tile = Rect((int(left), int(top)), (partitionRect.right - int(left), int(altsize)))
                            if color is not None and isInsideFilter(partitionRect, filter, tile.getPoint(USE_POINT_TO_CHECK_FILTER)):
                                self.__renderCache.append((tile, color))
                            top += altsize
                        missing_height: int = partitionRect.bottom - int(top)
                        left: float = partitionRect.left
                        while left + altsize < partitionRect.right:
                            color = self._renderData.colors[order[rowStartOrderIndex]] if order[rowStartOrderIndex] in  self._renderData.colors else partitionColor
                            filter = self._renderData.filters[order[rowStartOrderIndex]] if order[rowStartOrderIndex] in self._renderData.filters else partitionFilter
                            tile = Rect((int(left), int(top)), (int(altsize), missing_height))
                            if color is not None and isInsideFilter(partitionRect, filter, tile.getPoint(USE_POINT_TO_CHECK_FILTER)):
                                self.__renderCache.append((tile, color))
                            rowStartOrderIndex = (rowStartOrderIndex + 1) % len(order)
                            left += altsize
                        color = self._renderData.colors[order[rowStartOrderIndex]] if order[rowStartOrderIndex] in  self._renderData.colors else partitionColor
                        filter = self._renderData.filters[order[rowStartOrderIndex]] if order[rowStartOrderIndex] in self._renderData.filters else partitionFilter
                        tile = Rect((int(left), int(top)), (partitionRect.right - int(left), missing_height))
                        if color is not None and isInsideFilter(partitionRect, filter, tile.getPoint(USE_POINT_TO_CHECK_FILTER)):
                            self.__renderCache.append((tile, color))

                    case AltMode.STRIPED_H:
                        while top + altsize < partitionRect.bottom:
                            orderIndex = rowStartOrderIndex
                            left: float = partitionRect.left
                            while left + altsize < partitionRect.right:
                                color = self._renderData.colors[order[orderIndex]] if order[orderIndex] in self._renderData.colors else partitionColor
                                filter = self._renderData.filters[order[orderIndex]] if order[orderIndex] in self._renderData.filters else partitionFilter
                                tile = Rect((int(left), int(top)), (int(altsize), int(altsize)))
                                if color is not None and isInsideFilter(partitionRect, filter, tile.getPoint(USE_POINT_TO_CHECK_FILTER)):
                                    self.__renderCache.append((tile, color))
                                left += altsize
                            color = self._renderData.colors[order[orderIndex]] if order[orderIndex] in  self._renderData.colors else partitionColor
                            filter = self._renderData.filters[order[orderIndex]] if order[orderIndex] in self._renderData.filters else partitionFilter
                            tile = Rect((int(left), int(top)), (partitionRect.right - int(left), int(altsize)))
                            if color is not None and isInsideFilter(partitionRect, filter, tile.getPoint(USE_POINT_TO_CHECK_FILTER)):
                                self.__renderCache.append((tile, color))
                            rowStartOrderIndex = (rowStartOrderIndex + 1) % len(order)
                            top += altsize
                        missing_height: int = partitionRect.bottom - int(top)
                        left: float = partitionRect.left
                        while left + altsize < partitionRect.right:
                            color = self._renderData.colors[order[rowStartOrderIndex]] if order[rowStartOrderIndex] in  self._renderData.colors else partitionColor
                            filter = self._renderData.filters[order[rowStartOrderIndex]] if order[rowStartOrderIndex] in self._renderData.filters else partitionFilter
                            tile = Rect((int(left), int(top)), (int(altsize), missing_height))
                            if color is not None and isInsideFilter(partitionRect, filter, tile.getPoint(USE_POINT_TO_CHECK_FILTER)):
                                self.__renderCache.append((tile, color))
                            left += altsize
                        color = self._renderData.colors[order[rowStartOrderIndex]] if order[rowStartOrderIndex] in  self._renderData.colors else partitionColor
                        filter = self._renderData.filters[order[rowStartOrderIndex]] if order[rowStartOrderIndex] in self._renderData.filters else partitionFilter
                        tile = Rect((int(left), int(top)), (partitionRect.right - int(left), missing_height))
                        if color is not None and isInsideFilter(partitionRect, filter, tile.getPoint(USE_POINT_TO_CHECK_FILTER)):
                            self.__renderCache.append((tile, color))

                    case _:
                        if partitionColor is None:
                            continue
                        if not isinstance(partitionFilter, tuple):
                            self.__renderCache.append((partitionRect, partitionColor))
                            continue
                        while top + altsize < partitionRect.bottom:
                            left: float = partitionRect.left
                            while left + altsize < partitionRect.right:
                                tile = Rect((int(left), int(top)), (int(altsize), int(altsize)))
                                if partitionColor is not None and isInsideFilter(partitionRect, partitionFilter, tile.getPoint(USE_POINT_TO_CHECK_FILTER)):
                                    self.__renderCache.append((tile, partitionColor))
                                left += altsize
                            tile = Rect((int(left), int(top)), (partitionRect.right - int(left), int(altsize)))
                            if partitionColor is not None and isInsideFilter(partitionRect, partitionFilter, tile.getPoint(USE_POINT_TO_CHECK_FILTER)):
                                self.__renderCache.append((tile, partitionColor))
                            top += altsize
                        missing_height: int = partitionRect.bottom - int(top)
                        left: float = partitionRect.left
                        while left + altsize < partitionRect.right:
                            tile = Rect((int(left), int(top)), (int(altsize), missing_height))
                            if partitionColor is not None and isInsideFilter(partitionRect, partitionFilter, tile.getPoint(USE_POINT_TO_CHECK_FILTER)):
                                self.__renderCache.append((tile, partitionColor))
                            left += altsize
                        tile = Rect((int(left), int(top)), (partitionRect.right - int(left), missing_height))
                        if partitionColor is not None and isInsideFilter(partitionRect, partitionFilter, tile.getPoint(USE_POINT_TO_CHECK_FILTER)):
                            self.__renderCache.append((tile, partitionColor))



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

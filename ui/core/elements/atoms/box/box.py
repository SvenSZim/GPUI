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
    Box is a UI atom element for rendering rectangular shapes with various fill patterns and filters.

    The Box element supports:
    - Solid color fills
    - Partitioned sections with different colors
    - Pattern fills (checkerboard, vertical stripes, horizontal stripes)
    - Geometric filters (linear/triangular, quadratic/circular)
    - Partial insets for padding/margins
    - Complex render caching for performance

    Args:
        renderData (BoxData): Configuration data for rendering the box
        active (bool, optional): Whether the box is active and should be rendered. Defaults to True.
    """

    # -------------------- creation --------------------

    def __init__(self, renderData: BoxData, active: bool=True) -> None:
        self._validateType(renderData, BoxData, 'renderData')
        self._validateType(active, bool, 'active')
        super().__init__(BoxCore(), renderData, active)

        self.__renderCache = []
        EventManager.quickSubscribe(Body.getLayoutUpdateEvent(), self.updateRenderData)

    @override
    def copy(self) -> 'Box':
        """Create a deep copy of this Box element with its current state.

        Returns:
            Box: A new Box instance with copied render data and active state.
        """
        return Box(renderData=self._renderData.copy(), active=self.isActive())

    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'Box':
        return Box(renderData=BoxData.parseFromArgs(args))

    # -------------------- rendering --------------------

    __renderCache: list[tuple[Rect | tuple[tuple[int, int], tuple[int, int], int], Color]]

    def _validateRect(self, rect: Rect) -> Rect:
        """Validate and normalize a rectangle for rendering.

        Args:
            rect (Rect): The rectangle to validate

        Returns:
            Rect: Normalized rectangle with positive width and height

        Raises:
            TypeError: If rect is not a Rect instance
        """
        if not isinstance(rect, Rect):
            raise TypeError(f'rect must be a Rect instance, got {type(rect)}')

        # Normalize negative dimensions
        if rect.width < 0:
            rect = Rect((rect.left + rect.width, rect.top), (-rect.width, rect.height))
        if rect.height < 0:
            rect = Rect((rect.left, rect.top + rect.height), (rect.width, -rect.height))

        return rect

    def updateRenderData(self) -> None:
        """Update the cached render data based on current box configuration.

        This method pre-calculates all rendering information and stores it in
        the render cache for efficient drawing. It handles:
        - Rectangle normalization
        - Inset application
        - Partition processing
        - Pattern generation
        - Filter application
        """
        self.__renderCache = []

        #calculate render borderbox
        rect: Rect = self._validateRect(self.getRect())
        
        #apply partialInset
        def applyPartial(rect: Rect, partialInset: tuple[float, float] | float | tuple[int, int] | int) -> Rect:
            """Apply partial inset to a rectangle.

            Args:
                rect (Rect): The rectangle to apply inset to
                partialInset: Inset value(s) as float ratio or pixel counts

            Returns:
                Rect: New rectangle with inset applied

            Raises:
                TypeError: If parameters have invalid types
                ValueError: If inset values are invalid
            """
            if not isinstance(rect, Rect):
                raise TypeError(f'rect must be a Rect instance, got {type(rect)}')
            
            # Validate partialInset type and values
            if isinstance(partialInset, tuple):
                if len(partialInset) != 2:
                    raise ValueError('Tuple inset must have exactly 2 values')
                
                if isinstance(partialInset[0], (int, float)) and isinstance(partialInset[1], (int, float)):
                    if isinstance(partialInset[0], float):
                        if not 0 <= partialInset[0] <= 0.5 or not 0 <= partialInset[1] <= 0.5:
                            raise ValueError('Float insets must be between 0 and 0.5')
                else:
                    raise TypeError('Inset values must be int or float')
            elif not isinstance(partialInset, (int, float)):
                raise TypeError(f'partialInset must be tuple, int, or float, got {type(partialInset)}')
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
        def isInsideFilter(rect: Rect, filt: filtertype, point: tuple[int, int]) -> bool:
            """Check if a point is inside the filtered area of a rectangle.

            Args:
                rect (Rect): The rectangle to check against
                filt: Filter configuration (type, parameters, inversion)
                point: The point to test (x, y)

            Returns:
                bool: True if the point is inside the filtered area

            Raises:
                TypeError: If parameters have invalid types
                ValueError: If filter parameters are invalid
            """
            if not isinstance(rect, Rect):
                raise TypeError(f'rect must be a Rect instance, got {type(rect)}')
            if not isinstance(point, tuple) or len(point) != 2:
                raise TypeError('point must be a tuple of 2 integers')
            if not isinstance(point[0], int) or not isinstance(point[1], int):
                raise TypeError('point coordinates must be integers')

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
        """Render the Box onto the given surface using the cached render data.

        This method uses the pre-calculated render cache to efficiently draw the box
        with its current configuration of colors, patterns, and filters. The cache
        is updated whenever the box's layout changes.

        Args:
            surface (Surface): The target surface to render the box onto.

        Raises:
            AssertionError: If the drawer is not properly initialized or surface is invalid.
        """
        assert self._drawer is not None
        
        if self._active:
            for ob, color in self.__renderCache:
                if isinstance(ob, Rect):
                    self._drawer.drawrect(surface, ob, color)
                elif isinstance(ob, tuple):
                    self._drawer.drawline(surface, ob[0], ob[1], color, thickness=ob[2])

from typing import override
from numpy import sqrt

from .....utility import Rect
from .....display import Surface

from ..atom             import Atom
from .linecore          import LineCore
from .linedata          import LineData
from .linecreateoption  import LineCO
from .linecreator       import LineCreator
from .lineprefab        import LinePrefab
from .lineprefabmanager import LinePrefabManager


class Line(Atom[LineCore, LineData, LineCO, LinePrefab]):
    """
    Line is a simple ui-atom-element for drawing a line.
    """

    # -------------------- creation --------------------

    def __init__(self, rect: Rect, active: bool=True, renderStyleData: LinePrefab | list[LineCO] | LineData=LinePrefab.SOLID) -> None:
        assert self._renderstyle is not None

        if isinstance(renderStyleData, list):
            renderStyleData = LineCreator.createLineData(renderStyleData, self._renderstyle)
        elif isinstance(renderStyleData, LinePrefab):
            renderStyleData = LinePrefabManager.createLineData(renderStyleData, self._renderstyle)

        assert isinstance(renderStyleData, LineData)
        super().__init__(LineCore(rect), active, renderStyleData)

    @staticmethod
    @override
    def constructor(rect: Rect, active: bool=True, renderStyleData: LinePrefab | list[LineCO] | LineData=LinePrefab.SOLID) -> 'Line':
        return Line(rect, active=active, renderStyleData=renderStyleData)

    @staticmethod
    @override
    def fromCreateOptions(createOptions: list[LineCO]) -> 'Line':
        """
        fromCreateOptions creates the atom-element from createoptions.

        Args:
            createoptions (list[CreateOption]): the list of create-options to be used for creating

        Returns (this class): instance of the created atom
        """
        return Line(Rect(), renderStyleData=createOptions)

    @staticmethod
    @override
    def fromPrefab(prefab: LinePrefab) -> 'Line':
        """
        fromPrefab creates the atom-element from a prefab.

        Args:
            prefab (Prefab): the prefab to be created

        Returns (this class): instance of the created atom
        """
        return Line(Rect(), renderStyleData=prefab)

    # -------------------- rendering --------------------

    @override
    def render(self, surface: Surface) -> None:
        """
        render renders the Line onto the given surface

        Args:
            surface (Surface): the surface the Line should be drawn on
        """
        assert self._drawer is not None
        rect: Rect = self.getRect()

        # check if Element should be rendered
        if not self._active or (rect.width == 0 and rect.height == 0):
            return

        partial: float = self._renderData.partial
        rect_offset: tuple[int, int] = (int(0.5 * (1 - partial) * rect.width),
                                        int(0.5 * (1 - partial) * rect.height))
        rect = Rect((rect.left + rect_offset[0], rect.top + rect_offset[1]), (int(rect.width * partial), int(rect.height * partial)))

        # make rect have positive sizes
        if rect.width < 0:
            rect = Rect((rect.left + rect.width, rect.top), (-rect.width, rect.height))
        if rect.height < 0:
            rect = Rect((rect.left, rect.top + rect.height), (rect.width, -rect.height))
        boundRect: Rect = rect

        # flip -> mirror rect on y-axis
        if self._renderData.flip:
            rect = Rect((rect.left + rect.width, rect.top), (-rect.width, rect.height))

        if self._renderData.doAlt:
            assert self._renderData.altAbsLen is not None
            stepLength: float = self._renderData.altAbsLen
            normalizer: float = stepLength/sqrt(rect.width*rect.width + rect.height*rect.height)
            stepSizeX: float = rect.width*normalizer
            stepSizeY: float = rect.height*normalizer
            start_line: Rect = Rect(rect.getPosition(), (int(stepSizeX), int(stepSizeY)))
            firstColor: bool = True
            while boundRect.collidepoint((start_line.right, start_line.bottom)):
                if firstColor:
                    if self._renderData.mainColor is not None:
                        self._drawer.drawline(surface, (start_line.left, start_line.top), (start_line.right, start_line.bottom), self._renderData.mainColor)
                else:
                    if self._renderData.altColor is not None:
                        self._drawer.drawline(surface, (start_line.left, start_line.top), (start_line.right, start_line.bottom), self._renderData.altColor)
                firstColor = not firstColor
                start_line = Rect((start_line.right, start_line.bottom),(int(stepSizeX), int(stepSizeY)))
            if firstColor:
                if self._renderData.mainColor is not None:
                    self._drawer.drawline(surface, (start_line.left, start_line.top), (rect.right, rect.bottom), self._renderData.mainColor)
            else:
                if self._renderData.altColor is not None:
                    self._drawer.drawline(surface, (start_line.left, start_line.top), (rect.right, rect.bottom), self._renderData.altColor)



        elif self._renderData.mainColor is not None:
            self._drawer.drawline(surface, (rect.left, rect.top), (rect.right, rect.bottom), self._renderData.mainColor)



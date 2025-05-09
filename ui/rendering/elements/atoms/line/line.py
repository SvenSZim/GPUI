from typing import Any, override
from math import sqrt

from .....utility import Rect
from .....display import Surface

from ..atom             import Atom
from .linecore          import LineCore
from .linedata          import LineData
from .linecreateoption  import LineCO
from .lineprefab        import LinePrefab


class Line(Atom[LineCore, LineData, LineCO, LinePrefab]):
    """
    Line is a simple ui-atom-element for drawing a line.
    """

    # -------------------- creation --------------------

    def __init__(self, rect: Rect, renderData: LinePrefab | list[LineCO] | LineData=LinePrefab.SOLID, active: bool=True) -> None:
        assert self._renderstyle is not None

        if isinstance(renderData, list):
            myData: LineData = LineData()
            for createOption in renderData:
                myData += (createOption, self._renderstyle)
            renderData = myData
        elif isinstance(renderData, LinePrefab):
            renderData = LineData() * (renderData, self._renderstyle)

        assert isinstance(renderData, LineData)
        super().__init__(LineCore(rect), renderData, active)

    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'Line':
        return Line(Rect())

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

            cline: list[float] = [float(x) for x in rect.getPosition()]
            firstColor: bool = True
            while boundRect.collidepoint((int(cline[0] + stepSizeX), int(cline[1] + stepSizeY))):
                if firstColor:
                    if self._renderData.mainColor is not None:
                        self._drawer.drawline(surface, (int(cline[0]), int(cline[1])), (int(cline[0] + stepSizeX), int(cline[1] + stepSizeY)), self._renderData.mainColor)
                else:
                    if self._renderData.altColor is not None:
                        self._drawer.drawline(surface, (int(cline[0]), int(cline[1])), (int(cline[0] + stepSizeX), int(cline[1] + stepSizeY)), self._renderData.altColor)
                firstColor = not firstColor
                cline[0] += stepSizeX
                cline[1] += stepSizeY
            if firstColor:
                if self._renderData.mainColor is not None:
                    self._drawer.drawline(surface, (int(cline[0]), int(cline[1])), (rect.right, rect.bottom), self._renderData.mainColor)
            else:
                if self._renderData.altColor is not None:
                    self._drawer.drawline(surface, (int(cline[0]), int(cline[1])), (rect.right, rect.bottom), self._renderData.altColor)



        elif self._renderData.mainColor is not None:
            self._drawer.drawline(surface, (rect.left, rect.top), (rect.right, rect.bottom), self._renderData.mainColor)



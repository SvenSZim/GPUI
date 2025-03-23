from typing import Optional, override, Union
from numpy import sqrt

from ...generic import Rect, Color
from ...uidrawerinterface import UISurface

from ..uibody import UIABCBody
from ..UIABC import UIABC
from .UILineCore import UILineCore
from .UILineRenderData import UILineRenderData
from .UISLine import UISLine
from .UISLineCreateOptions import UISLineCreateOptions
from .UISLineCreator import UISLineCreator
from .UISLinePrefabs import UISLinePrefabs


class UILine(UIABC[UILineCore, UILineRenderData]):
    """
    UILineRender is the UIElementRender for all UILines.
    """

    def __init__(self, core: Union[UILineCore, UIABCBody, Rect], active: bool=True, renderStyleData: Union[UISLine, list[UISLineCreateOptions], UILineRenderData]=UISLine.SOLID) -> None:
        """
        __init__ initializes the UILineRender instance

        Args:
            core: UILine | UIABCBody | Rect = the refering UILine (Or UIABCBody bcs. they are 'equivalet')
            active: bool = active-state of the UILineRenderer
            renderStyleElement: UIStyledTexts = the render style that should be used when rendering styled
        """
        assert self._renderstyle is not None

        if not isinstance(core, UILineCore):
            core = UILineCore(core)

        if isinstance(renderStyleData, UISLine):
            renderStyleData = UISLinePrefabs.getPrefabRenderData(renderStyleData, self._renderstyle)
        elif isinstance(renderStyleData, list):
            renderStyleData = UISLineCreator.createStyledElement(renderStyleData, self._renderstyle)

        super().__init__(core, active, renderStyleData)

    @staticmethod
    @override
    def constructor(body: Union[UIABCBody, Rect], active: bool = True, renderStyleData: Union[UISLine, list[UISLineCreateOptions]] = UISLine.SOLID) -> 'UILine':
        return UILine(UILineCore(body), active=active, renderStyleData=renderStyleData)


    @override
    def render(self, surface: UISurface) -> None:
        """
        render renders the UILine onto the given surface

        Args:
            surface: UISurface = the surface the UILine should be drawn on
        """
        assert self._drawer is not None
        rect: Rect = self._core.getBody().getRect()

        # check if UIElement should be rendered
        if not self._active or (rect.width == 0 and rect.height == 0):
            return

        partial: float = self._renderData.partial
        rect_offset: tuple[int, int] = (int(0.5 * (1 - partial) * rect.width),
                                        int(0.5 * (1 - partial) * rect.height))
        rect = Rect((rect.left + rect_offset[0], rect.top + rect_offset[1]), (int(rect.width * partial), int(rect.height * partial)))

        color: Optional[Color] = self._renderData.mainColor


        if self._renderData.doAlt:
            assert self._renderData.altAbsLen is not None
            stepLength: float = self._renderData.altAbsLen
            normalizer: float = stepLength/sqrt(rect.width*rect.width + rect.height*rect.height)
            stepSizeX: float = rect.width*normalizer
            stepSizeY: float = rect.height*normalizer
            start_line: Rect = Rect(rect.getPosition(), (int(stepSizeX), int(stepSizeY)))
            firstColor: bool = True
            while rect.collidepoint((start_line.right, start_line.bottom)):
                if firstColor:
                    if color is not None:
                        self._drawer.drawline(surface, (start_line.left, start_line.top), (start_line.right, start_line.bottom), color)
                else:
                    if self._renderData.altColor is not None:
                        self._drawer.drawline(surface, (start_line.left, start_line.top), (start_line.right, start_line.bottom), self._renderData.altColor)
                firstColor = not firstColor
                start_line = Rect((start_line.right, start_line.bottom),(int(stepSizeX), int(stepSizeY)))
            if firstColor:
                if color is not None:
                    self._drawer.drawline(surface, (start_line.left, start_line.top), (rect.right, rect.bottom), color)
                else:
                    if self._renderData.altColor is not None:
                        self._drawer.drawline(surface, (start_line.left, start_line.top), (rect.right, rect.bottom), self._renderData.altColor)



        elif color is not None:
                self._drawer.drawline(surface, (rect.left, rect.top), (rect.right, rect.bottom), color)



from typing import Any, override

from ......utility   import Rect, AlignType
from ......display   import Surface
from ....element     import Element
from ....atoms       import AtomCreateOption, Box, Line
from ..addon         import Addon

from .framedcore         import FramedCore
from .frameddata         import FramedData
from .framedcreateoption import FramedCO
from .framedprefab       import FramedPrefab

class Framed(Addon[Element, FramedCore, FramedData, FramedCO, FramedPrefab]):

    __background: Box
    __borders: tuple[Line, Line, Line, Line]

    # -------------------- creation --------------------

    def __init__(self, inner: Element, offset: int=0, renderData: FramedPrefab | list[FramedCO | AtomCreateOption] | FramedData=FramedPrefab.BASIC, active: bool = True) -> None:
        assert self._renderstyle is not None

        if isinstance(renderData, list):
            myData: FramedData = FramedData()
            for createOption in renderData:
                myData += (createOption, self._renderstyle)
            renderData = myData
        elif isinstance(renderData, FramedPrefab):
            renderData = FramedData() * (renderData, self._renderstyle)

        super().__init__(FramedCore(inner, offset=offset), renderData, active)
        
        self.__background = Box(Rect(), renderData=self._renderData.fillData)
        self.__borders = (Line(Rect(), renderData=self._renderData.borderData[0]),
                          Line(Rect(), renderData=self._renderData.borderData[1]),
                          Line(Rect(), renderData=self._renderData.borderData[2]),
                          Line(Rect(), renderData=self._renderData.borderData[3]))
        self.__background.align(self)
        self.__background.alignSize(self)
        self.__borders[0].align(self)
        self.__borders[0].align(self, AlignType.iBL, keepSize=False)
        self.__borders[1].align(self, AlignType.iTiR)
        self.__borders[1].align(self, AlignType.iBR, keepSize=False)
        self.__borders[2].align(self)
        self.__borders[2].align(self, AlignType.TiR, keepSize=False)
        self.__borders[3].align(self, AlignType.iBiL)
        self.__borders[3].align(self, AlignType.BiR, keepSize=False)
    
    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'Framed':
        return Framed(args['inner'])

    # -------------------- rendering --------------------

    @override
    def render(self, surface: Surface) -> None:
        """
        render renders the UI-Element onto the given surface

        Args:
            surface (Surface): the surface the UIElement should be drawn on
        """
        assert self._drawer is not None
        
        # background
        if self._renderData.fillData is not None:
            self.__background.render(surface)

        # inner element
        self._core.getInner().render(surface)

        # outlines
        if self._renderData.borderData is not None:
            for border in self.__borders:
                border.render(surface)

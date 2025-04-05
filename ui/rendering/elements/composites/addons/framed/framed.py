from typing import override

from ......utility   import Rect
from ......display   import Surface
from .....createinfo import CreateInfo
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
            myData += (FramedCO.CREATE, self._renderstyle)
            renderData = myData
        elif isinstance(renderData, FramedPrefab):
            renderData = FramedData() * (renderData, self._renderstyle)

        super().__init__(FramedCore(inner, offset=offset), renderData, active)
        
        self.__background = self._renderData.fillData.createElement(Rect())
        self.__borders = (self._renderData.borderData[0].createElement(Rect()),
                          self._renderData.borderData[1].createElement(Rect()),
                          self._renderData.borderData[2].createElement(Rect()),
                          self._renderData.borderData[3].createElement(Rect()))
        self.__background.alignpoint(self)
        self.__background.alignpoint(self, (1,1),(1,1), keepSize=False)
        self.__borders[0].alignpoint(self)
        self.__borders[0].alignpoint(self, (1,1),(0,1), keepSize=False)
        self.__borders[1].alignpoint(self, (0,0), (1,0))
        self.__borders[1].alignpoint(self, (1,1),(1,1), keepSize=False)
        self.__borders[2].alignpoint(self)
        self.__borders[2].alignpoint(self, (1,1),(1,0), keepSize=False)
        self.__borders[3].alignpoint(self, (0,0), (0,1))
        self.__borders[3].alignpoint(self, (1,1),(1,1), keepSize=False)
    
    @staticmethod
    @override
    def fromCreateOptions(createOptions: list[FramedCO]) -> CreateInfo['Framed']:
        """
        fromCreateOptions creates the element from createoptions.

        Args:
            createoptions (list[CreateOption]): the list of create-options to be used for creating

        Returns (creator for this class): createinfo for this class
        """
        return CreateInfo(Framed, renderData=createOptions)

    @staticmethod
    @override
    def fromPrefab(prefab: FramedPrefab) -> CreateInfo['Framed']:
        """
        fromPrefab creates the element from a prefab.

        Args:
            prefab (Prefab): the prefab to be created

        Returns (creator for this class): createinfo for this class
        """
        return CreateInfo(Framed, renderData=prefab)

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

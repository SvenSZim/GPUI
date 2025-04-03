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

    # -------------------- creation --------------------

    def __init__(self, inner: Element, renderData: FramedPrefab | list[FramedCO | AtomCreateOption] | FramedData=FramedPrefab.BASIC, active: bool = True) -> None:
        assert self._renderstyle is not None

        if isinstance(renderData, list):
            myData: FramedData = FramedData()
            for createOption in renderData:
                myData += (createOption, self._renderstyle)
            renderData = myData
        elif isinstance(renderData, FramedPrefab):
            renderData = FramedData() * (renderData, self._renderstyle)

        super().__init__(inner, renderData, active)
    
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

    @staticmethod
    @override
    def _coreFromInner(inner: Element) -> FramedCore:
        return FramedCore(inner)

    # -------------------- rendering --------------------

    @override
    def render(self, surface: Surface) -> None:
        """
        render renders the UI-Element onto the given surface

        Args:
            surface (Surface): the surface the UIElement should be drawn on
        """
        assert self._drawer is not None
        rect: Rect = self.getRect()
        
        # background
        if self._renderData.fillData is not None:
            background: Box = self._renderData.fillData.createElement(rect)
            background.render(surface)

        # inner element
        self._core.getInner().render(surface)

        # outlines
        if self._renderData.borderData is not None:
            self._renderData.borderData[0].createElement(Rect(rect.getPosition(), (0, rect.height))).render(surface)
            self._renderData.borderData[1].createElement(Rect((rect.right, rect.top), (0, rect.height))).render(surface)
            self._renderData.borderData[2].createElement(Rect(rect.getPosition(), (rect.width, 0))).render(surface)
            self._renderData.borderData[3].createElement(Rect((rect.left, rect.bottom), (rect.width, 0))).render(surface)

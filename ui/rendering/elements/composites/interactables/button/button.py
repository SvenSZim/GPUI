from typing import override

from ......utility   import Rect
from ......display   import Surface
from .....createinfo import CreateInfo
from ....atoms       import AtomCreateOption, Box, Line
from ..interactable  import Interactable

from .buttoncore         import ButtonCore
from .buttondata         import ButtonData
from .buttoncreateoption import ButtonCO
from .buttonprefab       import ButtonPrefab

class Button(Interactable[ButtonCore, ButtonData, ButtonCO, ButtonPrefab]):

    __fillBox: Box
    __fillCross: tuple[Line, Line]

    # -------------------- creation --------------------

    def __init__(self, rect: Rect, buttonActive: bool=True,
                 renderData: ButtonPrefab | list[ButtonCO | AtomCreateOption] | ButtonData=ButtonPrefab.BASIC, active: bool = True) -> None:
        assert self._renderstyle is not None

        if isinstance(renderData, list):
            myData: ButtonData = ButtonData()
            for createOption in renderData:
                myData += (createOption, self._renderstyle)
            myData += (ButtonCO.CREATE, self._renderstyle)
            renderData = myData
        elif isinstance(renderData, ButtonPrefab):
            renderData = ButtonData() * (renderData, self._renderstyle)

        super().__init__(ButtonCore(rect, buttonActive), renderData, active)
        assert self._renderData.fillData is not None or self._renderData.borderData is not None

        self.__fillBox   = self._renderData.fillData.createElement(rect)
        self.__fillCross = (self._renderData.crossData[0].createElement(rect),
                            self._renderData.crossData[1].createElement(rect))
        self.__fillBox.alignpoint(self)
        self.__fillCross[0].alignpoint(self)
        self.__fillCross[1].alignpoint(self)
    
    @staticmethod
    @override
    def fromCreateOptions(createOptions: list[ButtonCO]) -> CreateInfo['Button']:
        """
        fromCreateOptions creates the element from createoptions.

        Args:
            createoptions (list[CreateOption]): the list of create-options to be used for creating

        Returns (creator for this class): createinfo for this class
        """
        return CreateInfo(Button, renderData=createOptions)

    @staticmethod
    @override
    def fromPrefab(prefab: ButtonPrefab) -> CreateInfo['Button']:
        """
        fromPrefab creates the element from a prefab.

        Args:
            prefab (Prefab): the prefab to be created

        Returns (creator for this class): createinfo for this class
        """
        return CreateInfo(Button, renderData=prefab)

    # -------------------- rendering --------------------

    @override
    def render(self, surface: Surface) -> None:
        """
        render renders the UI-Element onto the given surface

        Args:
            surface (Surface): the surface the UIElement should be drawn on
        """
        assert self._drawer is not None

        if self._core.isPressed():
            self.__fillBox.render(surface)
            self.__fillCross[0].render(surface)
            self.__fillCross[1].render(surface)

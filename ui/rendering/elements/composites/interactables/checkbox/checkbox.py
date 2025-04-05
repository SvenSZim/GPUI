from typing import override

from ......utility   import Rect
from ......display   import Surface
from .....createinfo import CreateInfo
from ....atoms       import AtomCreateOption, Box, Line
from ..interactable  import Interactable

from .checkboxcore         import CheckboxCore
from .checkboxdata         import CheckboxData
from .checkboxcreateoption import CheckboxCO
from .checkboxprefab       import CheckboxPrefab

class Checkbox(Interactable[CheckboxCore, CheckboxData, CheckboxCO, CheckboxPrefab]):

    __fillBox: Box
    __fillCross: tuple[Line, Line]

    # -------------------- creation --------------------

    def __init__(self, rect: Rect, startState: bool=False, checkboxActive: bool=True,
                 renderData: CheckboxPrefab | list[CheckboxCO | AtomCreateOption] | CheckboxData=CheckboxPrefab.BASIC, active: bool = True) -> None:
        assert self._renderstyle is not None

        if isinstance(renderData, list):
            myData: CheckboxData = CheckboxData()
            for createOption in renderData:
                myData += (createOption, self._renderstyle)
            myData += (CheckboxCO.CREATE, self._renderstyle)
            renderData = myData
        elif isinstance(renderData, CheckboxPrefab):
            renderData = CheckboxData() * (renderData, self._renderstyle)

        super().__init__(CheckboxCore(rect, startState, checkboxActive), renderData, active)
        assert self._renderData.fillData is not None or self._renderData.borderData is not None

        self.__fillBox   = self._renderData.fillData.createElement(rect)
        self.__fillCross = (self._renderData.crossData[0].createElement(rect),
                            self._renderData.crossData[1].createElement(rect))
        self.__fillBox.alignpoint(self)
        self.__fillCross[0].alignpoint(self)
        self.__fillCross[1].alignpoint(self)
    
    @staticmethod
    @override
    def fromCreateOptions(createOptions: list[CheckboxCO]) -> CreateInfo['Checkbox']:
        """
        fromCreateOptions creates the element from createoptions.

        Args:
            createoptions (list[CreateOption]): the list of create-options to be used for creating

        Returns (creator for this class): createinfo for this class
        """
        return CreateInfo(Checkbox, renderData=createOptions)

    @staticmethod
    @override
    def fromPrefab(prefab: CheckboxPrefab) -> CreateInfo['Checkbox']:
        """
        fromPrefab creates the element from a prefab.

        Args:
            prefab (Prefab): the prefab to be created

        Returns (creator for this class): createinfo for this class
        """
        return CreateInfo(Checkbox, renderData=prefab)

    # -------------------- rendering --------------------

    @override
    def render(self, surface: Surface) -> None:
        """
        render renders the UI-Element onto the given surface

        Args:
            surface (Surface): the surface the UIElement should be drawn on
        """
        assert self._drawer is not None

        if self._core.getCurrentToggleState():
            self.__fillBox.render(surface)
            self.__fillCross[0].render(surface)
            self.__fillCross[1].render(surface)

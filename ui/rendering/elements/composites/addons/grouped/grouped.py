from typing import override

from ......utility   import Rect
from ......display   import Surface
from .....createinfo import CreateInfo
from ....element     import Element
from ....atoms       import AtomCreateOption
from ..addon         import Addon

from .groupedcore         import GroupedCore
from .groupeddata         import GroupedData
from .groupedcreateoption import GroupedCO
from .groupedprefab       import GroupedPrefab

class Grouped(Addon[list[Element], GroupedCore, GroupedData, GroupedCO, GroupedPrefab]):

    

    # -------------------- creation --------------------

    def __init__(self, rect: Rect, *inner: Element | tuple[Element, float], alignVertical: bool=True, offset: int=0,
                 renderData: GroupedPrefab | list[GroupedCO | AtomCreateOption] | GroupedData=GroupedPrefab.BASIC, active: bool = True) -> None:
        assert self._renderstyle is not None

        if isinstance(renderData, list):
            myData: GroupedData = GroupedData()
            for createOption in renderData:
                myData += (createOption, self._renderstyle)
            myData += (GroupedCO.CREATE, self._renderstyle)
            renderData = myData
        elif isinstance(renderData, GroupedPrefab):
            renderData = GroupedData() * (renderData, self._renderstyle)

        super().__init__(GroupedCore(rect, *inner, alignVertical=alignVertical, offset=offset), renderData, active)
    
    @staticmethod
    @override
    def fromCreateOptions(createOptions: list[GroupedCO]) -> CreateInfo['Grouped']:
        """
        fromCreateOptions creates the element from createoptions.

        Args:
            createoptions (list[CreateOption]): the list of create-options to be used for creating

        Returns (creator for this class): createinfo for this class
        """
        return CreateInfo(Grouped, renderData=createOptions)

    @staticmethod
    @override
    def fromPrefab(prefab: GroupedPrefab) -> CreateInfo['Grouped']:
        """
        fromPrefab creates the element from a prefab.

        Args:
            prefab (Prefab): the prefab to be created

        Returns (creator for this class): createinfo for this class
        """
        return CreateInfo(Grouped, renderData=prefab)

    # -------------------- rendering --------------------

    @override
    def render(self, surface: Surface) -> None:
        """
        render renders the UI-Element onto the given surface

        Args:
            surface (Surface): the surface the UIElement should be drawn on
        """
        assert self._drawer is not None

        for el in self._core.getInner():
            el.render(surface)

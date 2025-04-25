from typing import override

from ......utility   import Rect
from ......display   import Surface
from .....createinfo import CreateInfo
from ....element     import Element
from ....atoms       import AtomCreateOption
from ..addon         import Addon

from .stackcore         import StackCore
from .stackdata         import StackData
from .stackcreateoption import StackCO
from .stackprefab       import StackPrefab

class Stack(Addon[list[Element], StackCore, StackData, StackCO, StackPrefab]):

    

    # -------------------- creation --------------------

    def __init__(self, rect: Rect, elementSizing: Rect, *inner: Element | tuple[Element, float], alignVertical: bool=True, offset: int=0,
                 renderData: StackPrefab | list[StackCO | AtomCreateOption] | StackData=StackPrefab.BASIC, active: bool = True) -> None:
        assert self._renderstyle is not None

        if isinstance(renderData, list):
            myData: StackData = StackData()
            for createOption in renderData:
                myData += (createOption, self._renderstyle)
            myData += (StackCO.CREATE, self._renderstyle)
            renderData = myData
        elif isinstance(renderData, StackPrefab):
            renderData = StackData() * (renderData, self._renderstyle)

        super().__init__(StackCore(rect, elementSizing, *inner, alignVertical=alignVertical, offset=offset), renderData, active)
    
    @staticmethod
    @override
    def fromCreateOptions(createOptions: list[StackCO]) -> CreateInfo['Stack']:
        """
        fromCreateOptions creates the element from createoptions.

        Args:
            createoptions (list[CreateOption]): the list of create-options to be used for creating

        Returns (creator for this class): createinfo for this class
        """
        return CreateInfo(Stack, renderData=createOptions)

    @staticmethod
    @override
    def fromPrefab(prefab: StackPrefab) -> CreateInfo['Stack']:
        """
        fromPrefab creates the element from a prefab.

        Args:
            prefab (Prefab): the prefab to be created

        Returns (creator for this class): createinfo for this class
        """
        return CreateInfo(Stack, renderData=prefab)

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

from typing import Any, override

from ......utility   import Rect
from ......display   import Surface
from ....element     import Element
from ....atoms       import AtomCreateOption
from ..addon         import Addon

from .stackedcore         import StackedCore
from .stackeddata         import StackedData
from .stackedcreateoption import StackedCO
from .stackedprefab       import StackedPrefab

class Stacked(Addon[list[Element], StackedCore, StackedData, StackedCO, StackedPrefab]):

    

    # -------------------- creation --------------------

    def __init__(self, rect: Rect, elementSizing: Rect, *inner: Element | tuple[Element, float], alignVertical: bool=True, offset: int=0,
                 renderData: StackedPrefab | list[StackedCO | AtomCreateOption] | StackedData=StackedPrefab.BASIC, active: bool = True) -> None:
        assert self._renderstyle is not None

        if isinstance(renderData, list):
            myData: StackedData = StackedData()
            for createOption in renderData:
                myData += (createOption, self._renderstyle)
            myData += (StackedCO.CREATE, self._renderstyle)
            renderData = myData
        elif isinstance(renderData, StackedPrefab):
            renderData = StackedData() * (renderData, self._renderstyle)

        super().__init__(StackedCore(rect, elementSizing, *inner, alignVertical=alignVertical, offset=offset), renderData, active)
    
    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'Stacked':
        return Stacked(Rect(), Rect())

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

from typing import Any, override

from ......utility   import Rect
from ......display   import Surface
from ....element     import Element
from ..addon         import Addon

from .stackedcore         import StackedCore
from .stackeddata         import StackedData

class Stacked(Addon[StackedCore, StackedData]):
    
    # -------------------- creation --------------------

    def __init__(self, rect: Rect, elementSizing: Rect, *inner: Element | tuple[Element, float], alignVertical: bool=True, offset: int=0, active: bool = True) -> None:
        super().__init__(StackedCore(rect, elementSizing, *inner, alignVertical=alignVertical, offset=offset), StackedData(), active)
    
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

        if self.isActive():
            self._core.getInner().render(surface)

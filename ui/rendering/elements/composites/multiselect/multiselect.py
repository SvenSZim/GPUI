from typing import Any, Callable, Optional, override

from .....utility   import Rect
from .....display   import Surface
from ...element     import Element
from ..composition  import Composition

from .multiselectcore         import MultiselectCore
from .multiselectdata         import MultiselectData
from .multiselectcreateoption import MultiselectCO
from .multiselectprefab       import MultiselectPrefab

class Multiselect(Composition[MultiselectCore, MultiselectData, MultiselectCO, MultiselectPrefab]):

    # -------------------- creation --------------------

    def __init__(self, rect: Rect, *inner: Element | tuple[Element, float], alignVertical: bool=True, offset: int=0,
                 startState: int=0, restriction: Optional[Callable[[int], int]]=None,
                 renderData: MultiselectPrefab | list[MultiselectCO] | MultiselectData=MultiselectPrefab.BASIC, active: bool = True) -> None:
        assert self._renderstyle is not None

        if isinstance(renderData, list):
            myData: MultiselectData = MultiselectData()
            for createOption in renderData:
                myData += (createOption, self._renderstyle)
            renderData = myData
        elif isinstance(renderData, MultiselectPrefab):
            renderData = MultiselectData() * (renderData, self._renderstyle)

        super().__init__(MultiselectCore(rect, *inner, alignVertical=alignVertical, offset=offset, startState=startState, restriction=restriction), renderData, active)
    
    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'Multiselect':
        return Multiselect(Rect())

    # -------------------- subscriptions --------------------
    
    #MISSING

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

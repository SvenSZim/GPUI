from typing import Any, Callable, Optional, override

from .....utility   import Rect
from .....display   import Surface
from ....createinfo import CreateInfo
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
            myData += (MultiselectCO.CREATE, self._renderstyle)
            renderData = myData
        elif isinstance(renderData, MultiselectPrefab):
            renderData = MultiselectData() * (renderData, self._renderstyle)

        super().__init__(MultiselectCore(rect, *inner, alignVertical=alignVertical, offset=offset, startState=startState, restriction=restriction), renderData, active)
    
    @staticmethod
    @override
    def fromCreateOptions(createOptions: list[MultiselectCO]) -> CreateInfo['Multiselect']:
        """
        fromCreateOptions creates the element from createoptions.

        Args:
            createoptions (list[CreateOption]): the list of create-options to be used for creating

        Returns (creator for this class): createinfo for this class
        """
        return CreateInfo(Multiselect, renderData=createOptions)

    @staticmethod
    @override
    def fromPrefab(prefab: MultiselectPrefab) -> CreateInfo['Multiselect']:
        """
        fromPrefab creates the element from a prefab.

        Args:
            prefab (Prefab): the prefab to be created

        Returns (creator for this class): createinfo for this class
        """
        return CreateInfo(Multiselect, renderData=prefab)

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

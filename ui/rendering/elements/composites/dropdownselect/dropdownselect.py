from typing import Any, Callable, override

from .....utility   import Rect
from .....display   import Surface
from ....createinfo import CreateInfo
from ...element     import Element
from ..composition  import Composition

from .dropdownselectcore         import DropdownselectCore
from .dropdownselectdata         import DropdownselectData
from .dropdownselectcreateoption import DropdownselectCO
from .dropdownselectprefab       import DropdownselectPrefab

class Dropdownselect(Composition[DropdownselectCore, DropdownselectData, DropdownselectCO, DropdownselectPrefab]):

    # -------------------- creation --------------------

    def __init__(self, rect: Rect, *inner: tuple[Element | tuple[Element, float], Element], verticalDropdown: bool=True, offset: int=0, startState: int=0,
                 renderData: DropdownselectPrefab | list[DropdownselectCO] | DropdownselectData=DropdownselectPrefab.BASIC, active: bool = True) -> None:
        assert self._renderstyle is not None

        if isinstance(renderData, list):
            myData: DropdownselectData = DropdownselectData()
            for createOption in renderData:
                myData += (createOption, self._renderstyle)
            myData += (DropdownselectCO.CREATE, self._renderstyle)
            renderData = myData
        elif isinstance(renderData, DropdownselectPrefab):
            renderData = DropdownselectData() * (renderData, self._renderstyle)

        super().__init__(DropdownselectCore(rect, *inner, verticalDropdown=verticalDropdown, offset=offset, startState=startState), renderData, active)
    
    @staticmethod
    @override
    def fromCreateOptions(createOptions: list[DropdownselectCO]) -> CreateInfo['Dropdownselect']:
        """
        fromCreateOptions creates the element from createoptions.

        Args:
            createoptions (list[CreateOption]): the list of create-options to be used for creating

        Returns (creator for this class): createinfo for this class
        """
        return CreateInfo(Dropdownselect, renderData=createOptions)

    @staticmethod
    @override
    def fromPrefab(prefab: DropdownselectPrefab) -> CreateInfo['Dropdownselect']:
        """
        fromPrefab creates the element from a prefab.

        Args:
            prefab (Prefab): the prefab to be created

        Returns (creator for this class): createinfo for this class
        """
        return CreateInfo(Dropdownselect, renderData=prefab)

    # -------------------- subscriptions --------------------
    
    def subscribeToStateChange(self, callback: str) -> bool:
        """
        subscribeToStateChange subscribes a Callback to the Event of the object
        getting clicked.

        Args:
            callback (str): the id of the callback to subscribe to the click

        Returns (bool): returns if the subscription was successful
        """
        return self._core.subscribeToClick(callback)
    
    def unsubscribeToStateChange(self, callback: str) -> bool:
        """
        unsubscribeToStateChange unsubscribes a callback (by id) from the Event of the
        object getting clicked.

        Args:
            callback (str): the id of the callback to unsubscribe

        Returns (bool): if the unsubscription was successful
        """
        return self._core.unsubscribeToClick(callback)

    def quickSubscribeToStateChange(self, f: Callable, *args: Any) -> tuple[str, bool]:
        """
        quickSubscribeToStateChange takes a function and its arguments, creates
        a Callback and subscribes to the Event of the object getting clicked.

        Args:
            f     (Callable) : the function to use as callback
            args  (list[Any]): the arguments to use as callback

        Returns (tuple[str, bool]): 1. the id of the newly created Callback
                                    2. if the callback was successfully subscribed
        """
        return self._core.quickSubscribeToClick(f, *args)
    
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
            self._core.getDropdown().render(surface)
            self._core.getOuter().render(surface)

from typing import Any, Callable, override

from ......display   import Surface
from .....createinfo import CreateInfo
from ....element     import Element
from ....atoms       import AtomCreateOption
from ..interactable  import Interactable

from .clickwrappercore         import ClickwrapperCore
from .clickwrapperdata         import ClickwrapperData
from .clickwrappercreateoption import ClickwrapperCO
from .clickwrapperprefab       import ClickwrapperPrefab

class Clickwrapper(Interactable[ClickwrapperCore, ClickwrapperData, ClickwrapperCO, ClickwrapperPrefab]):

    # -------------------- creation --------------------

    def __init__(self, inner: Element, buttonActive: bool=True,
                 renderData: ClickwrapperPrefab | list[ClickwrapperCO | AtomCreateOption] | ClickwrapperData=ClickwrapperPrefab.BASIC, active: bool = True) -> None:
        assert self._renderstyle is not None

        if isinstance(renderData, list):
            myData: ClickwrapperData = ClickwrapperData()
            for createOption in renderData:
                myData += (createOption, self._renderstyle)
            myData += (ClickwrapperCO.CREATE, self._renderstyle)
            renderData = myData
        elif isinstance(renderData, ClickwrapperPrefab):
            renderData = ClickwrapperData() * (renderData, self._renderstyle)

        super().__init__(ClickwrapperCore(inner, buttonActive), renderData, renderActive=active, buttonActive=buttonActive)
    
    @staticmethod
    @override
    def fromCreateOptions(createOptions: list[ClickwrapperCO]) -> CreateInfo['Clickwrapper']:
        """
        fromCreateOptions creates the element from createoptions.

        Args:
            createoptions (list[CreateOption]): the list of create-options to be used for creating

        Returns (creator for this class): createinfo for this class
        """
        return CreateInfo(Clickwrapper, renderData=createOptions)

    @staticmethod
    @override
    def fromPrefab(prefab: ClickwrapperPrefab) -> CreateInfo['Clickwrapper']:
        """
        fromPrefab creates the element from a prefab.

        Args:
            prefab (Prefab): the prefab to be created

        Returns (creator for this class): createinfo for this class
        """
        return CreateInfo(Clickwrapper, renderData=prefab)

    # -------------------- active-state --------------------

    @override
    def setButtonActive(self, buttonActive: bool) -> None:
        self._core.setButtonActive(buttonActive)
        return super().setButtonActive(buttonActive)

    @override
    def toggleButtonActive(self) -> bool:
        self._core.toggleButtonActive()
        return super().toggleButtonActive()


    # -------------------- subscriptions --------------------

    @override
    def subscribeToClick(self, callback: str) -> bool:
        """
        subscribeToClick subscribes a Callback to the Event of the object
        getting clicked.

        Args:
            callback (str): the id of the callback to subscribe to the click

        Returns (bool): returns if the subscription was successful
        """
        return self._core.subscribeToClick(callback)
    
    @override
    def unsubscribeToClick(self, callback: str) -> bool:
        """
        unsubscribeToClick unsubscribes a callback (by id) from the Event of the
        object getting clicked.

        Args:
            callback (str): the id of the callback to unsubscribe

        Returns (bool): if the unsubscription was successful
        """
        return self._core.unsubscribeToClick(callback)

    @override
    def quickSubscribeToClick(self, f: Callable, *args: Any) -> tuple[str, bool]:
        """
        quickSubscribeToClick takes a function and its arguments, creates
        a Callback and subscribes to the Event of the object getting clicked.

        Args:
            f     (Callable) : the function to use as callback
            args  (list[Any]): the arguments to use as callback

        Returns (tuple[str, bool]): 1. the id of the newly created Callback
                                    2. if the callback was successfully subscribed
        """
        return self._core.quickSubscribeToClick(f, *args)

    def subscribeToHold(self, callback: str) -> bool:
        """
        subscribeToHold subscribes a Callback to the Event of the button
        getting pressed down.

        Args:
            callback (str): the id of the callback to subscribe to the click

        Returns (bool): returns if the subscription was successful
        """
        return self._core.subscribeToHold(callback)
    
    def unsubscribeToHold(self, callback: str) -> bool:
        """
        unsubscribeToHold unsubscribes a callback (by id) from the Event of the
        button getting pressed down.

        Args:
            callback (str): the id of the callback to unsubscribe

        Returns (bool): if the unsubscription was successful
        """
        return self._core.unsubscribeToHold(callback)

    def quickSubscribeToHold(self, f: Callable, *args: Any) -> tuple[str, bool]:
        """
        quickSubscribeToHold takes a function and its arguments, creates
        a Callback and subscribes to the Event of the button getting pressed down.

        Args:
            f     (Callable) : the function to use as callback
            args  (list[Any]): the arguments to use as callback

        Returns (tuple[str, bool]): 1. the id of the newly created Callback
                                    2. if the callback was successfully subscribed
        """
        return self._core.quickSubscribeToHold(f, *args)

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

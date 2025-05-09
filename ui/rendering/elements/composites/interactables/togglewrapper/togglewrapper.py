from typing import Any, Callable, override

from ......display   import Surface
from ....element     import Element
from ....atoms       import AtomCreateOption
from ..interactable  import Interactable

from .togglewrappercore         import TogglewrapperCore
from .togglewrapperdata         import TogglewrapperData
from .togglewrappercreateoption import TogglewrapperCO
from .togglewrapperprefab       import TogglewrapperPrefab

class Togglewrapper(Interactable[TogglewrapperCore, TogglewrapperData, TogglewrapperCO, TogglewrapperPrefab]):

    # -------------------- creation --------------------

    def __init__(self, inner: Element, numberOfStates: int=2, startState: int=0, buttonActive: bool=True,
                 renderData: TogglewrapperPrefab | list[TogglewrapperCO | AtomCreateOption] | TogglewrapperData=TogglewrapperPrefab.BASIC, active: bool = True) -> None:
        assert self._renderstyle is not None

        if isinstance(renderData, list):
            myData: TogglewrapperData = TogglewrapperData()
            for createOption in renderData:
                myData += (createOption, self._renderstyle)
            renderData = myData
        elif isinstance(renderData, TogglewrapperPrefab):
            renderData = TogglewrapperData() * (renderData, self._renderstyle)

        super().__init__(TogglewrapperCore(inner, numberOfStates, startState, buttonActive), renderData, renderActive=active, buttonActive=buttonActive)
    
    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'Togglewrapper':
        return Togglewrapper(args['inner'])

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

    def subscribeToToggleState(self, state: int, callback: str) -> bool:
        """
        subscribeToToggleState subscribes a Callback to the triggerEvent of the
        given toggleState of the Toggle.

        Args:
            state    (int): the toggleState the Callback should be subscribed to
            callback (str): the id of the callback to subscribe to toggleState

        Returns (bool): returns if the subscription was successful
        """
        return self._core.subscribeToToggleState(state, callback)

    def unsubscribeToToggleState(self, state: int, callback: str) -> bool:
        """
        unsubscribeToToggleState unsubscribes a callback (by id) from the Event of the
        toggle being in a given state.

        Args:
            state    (int): the toggleState the Callback should be unsubscribed from
            callback (str): the id of the callback to unsubscribe

        Returns (bool): if the unsubscription was successful
        """
        return self._core.unsubscribeToToggleState(state, callback)

    def quickSubscribeToToggleState(self, state: int, f: Callable, *args: Any) -> tuple[str, bool]:
        """
        quickSubscribeToToggleState takes a function and its arguments, creates
        a Callback and subscribes to the Event of the toggle being in a given state.

        Args:
            state (int)      : the toggleState the function should subscribe to
            f     (Callable) : the function to use as callback
            args  (list[Any]): the arguments to use as callback

        Returns (tuple[str, bool]): 1. the id of the newly created Callback
                                    2. if the callback was successfully subscribed
        """
        return self._core.quickSubscribeToToggleState(state, f, *args)

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
            if self._core.getCurrentToggleState():
                self._drawer.drawrect(surface, self.getRect(), 'green')
            self._core.getInner().render(surface)

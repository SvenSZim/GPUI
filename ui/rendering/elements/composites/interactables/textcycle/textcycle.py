from typing import Any, Callable, override

from ......utility   import Rect
from ......display   import Surface
from ....atoms       import AtomCreateOption, Text
from ..interactable  import Interactable

from .textcyclecore         import TextCycleCore
from .textcycledata         import TextCycleData
from .textcyclecreateoption import TextCycleCO
from .textcycleprefab       import TextCyclePrefab

class TextCycle(Interactable[TextCycleCore, TextCycleData, TextCycleCO, TextCyclePrefab]):

    __text: Text

    # -------------------- creation --------------------

    def __init__(self, rect: Rect, contents: list[str], startState: int=0, textcycleActive: bool=True,
                 renderData: TextCyclePrefab | list[TextCycleCO | AtomCreateOption] | TextCycleData=TextCyclePrefab.BASIC, active: bool = True) -> None:
        assert self._renderstyle is not None

        if isinstance(renderData, list):
            myData: TextCycleData = TextCycleData()
            for createOption in renderData:
                myData += (createOption, self._renderstyle)
            renderData = myData
        elif isinstance(renderData, TextCyclePrefab):
            renderData = TextCycleData() * (renderData, self._renderstyle)

        super().__init__(TextCycleCore(rect, contents, startState, textcycleActive), renderData, active)

        self.__text = Text(Rect(), self._core.getContent(), renderData=self._renderData.textData)
        self.__text.align(self)
        self.__text.alignSize(self)
    
    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'TextCycle':
        return TextCycle(Rect(), [])

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

    def subscribeToState(self, state: int, callback: str) -> bool:
        """
        subscribeToState subscribes a Callback to the textcycle being selected.
        
        Args:
            state    (int): the state to subscribe the callback to
            callback (str): the id of the callback to subscribe to the selection

        Returns (bool): returns if the subscription was successful
        """
        return self._core.subscribeToToggleState(state, callback)

    def unsubscribeToState(self, state: int, callback: str) -> bool:
        """
        unsubscribeToState unsubscribes a callback (by id) from the textcycle being selected
        
        Args:
            state    (int): the state to unsubscribe the callback from
            callback (str): the id of the callback to unsubscribe

        Returns (bool): if the unsubscription was successful
        """
        return self._core.unsubscribeToToggleState(state, callback)

    def quickSubscribeToState(self, state: int, f: Callable, *args: Any) -> tuple[str, bool]:
        """
        quickSubscribeToToggleState takes a function and its arguments, creates
        a Callback and subscribes to the textcycle being selected.

        Args:
            state (int)      : the state to quick subscribe to
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

        if not self._active:
            return
    
        self.__text.updateContent(self._core.getContent())
        self.__text.render(surface)

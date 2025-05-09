from typing import Any, Callable, override

from ......utility   import Rect
from ......display   import Surface
from ....atoms       import AtomCreateOption, Box, Line
from ..interactable  import Interactable

from .checkboxcore         import CheckboxCore
from .checkboxdata         import CheckboxData
from .checkboxcreateoption import CheckboxCO
from .checkboxprefab       import CheckboxPrefab

class Checkbox(Interactable[CheckboxCore, CheckboxData, CheckboxCO, CheckboxPrefab]):

    __fillBox: Box
    __fillCross: tuple[Line, Line]

    # -------------------- creation --------------------

    def __init__(self, rect: Rect, startState: bool=False, checkboxActive: bool=True,
                 renderData: CheckboxPrefab | list[CheckboxCO | AtomCreateOption] | CheckboxData=CheckboxPrefab.BASIC, active: bool = True) -> None:
        assert self._renderstyle is not None

        if isinstance(renderData, list):
            myData: CheckboxData = CheckboxData()
            for createOption in renderData:
                myData += (createOption, self._renderstyle)
            myData += (CheckboxCO.CREATE, self._renderstyle)
            renderData = myData
        elif isinstance(renderData, CheckboxPrefab):
            renderData = CheckboxData() * (renderData, self._renderstyle)

        super().__init__(CheckboxCore(rect, startState, checkboxActive), renderData, active)

        self.__fillBox   = Box(Rect(), renderData=self._renderData.fillData)
        self.__fillCross = (Line(Rect(), renderData=self._renderData.crossData[0]),
                            Line(Rect(), renderData=self._renderData.crossData[1]))
        self.__fillBox.align(self)
        self.__fillBox.alignSize(self)
        self.__fillCross[0].align(self)
        self.__fillCross[0].alignSize(self)
        self.__fillCross[1].align(self)
        self.__fillCross[1].alignSize(self)
    
    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'Checkbox':
        return Checkbox(Rect())

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

    def subscribeToSelect(self, callback: str) -> bool:
        """
        subscribeToSelect subscribes a Callback to the checkbox being selected.
        Args:
            callback (str): the id of the callback to subscribe to the selection

        Returns (bool): returns if the subscription was successful
        """
        return self._core.subscribeToToggleState(1, callback)

    def unsubscribeToSelect(self, callback: str) -> bool:
        """
        unsubscribeToSelect unsubscribes a callback (by id) from the checkbox being selected
        Args:
            callback (str): the id of the callback to unsubscribe

        Returns (bool): if the unsubscription was successful
        """
        return self._core.unsubscribeToToggleState(1, callback)

    def quickSubscribeToSelect(self, f: Callable, *args: Any) -> tuple[str, bool]:
        """
        quickSubscribeToToggleState takes a function and its arguments, creates
        a Callback and subscribes to the checkbox being selected.

        Args:
            f     (Callable) : the function to use as callback
            args  (list[Any]): the arguments to use as callback

        Returns (tuple[str, bool]): 1. the id of the newly created Callback
                                    2. if the callback was successfully subscribed
        """
        return self._core.quickSubscribeToToggleState(1, f, *args)

    def subscribeToDeselect(self, callback: str) -> bool:
        """
        subscribeToDeselect subscribes a Callback to the checkbox being deselected.
        
        Args:
            callback (str): the id of the callback to subscribe to the deselection

        Returns (bool): returns if the subscription was successful
        """
        return self._core.subscribeToToggleState(0, callback)

    def unsubscribeToDeselect(self, callback: str) -> bool:
        """
        unsubscribeToDeselect unsubscribes a callback (by id) from the checkbox being deselected
        
        Args:
            callback (str): the id of the callback to unsubscribe

        Returns (bool): if the unsubscription was successful
        """
        return self._core.unsubscribeToToggleState(0, callback)

    def quickSubscribeToDeselect(self, f: Callable, *args: Any) -> tuple[str, bool]:
        """
        quickSubscribeToDeselect takes a function and its arguments, creates
        a Callback and subscribes to the checkbox being deselected.

        Args:
            f     (Callable) : the function to use as callback
            args  (list[Any]): the arguments to use as callback

        Returns (tuple[str, bool]): 1. the id of the newly created Callback
                                    2. if the callback was successfully subscribed
        """
        return self._core.quickSubscribeToToggleState(0, f, *args)

    # -------------------- rendering --------------------

    @override
    def render(self, surface: Surface) -> None:
        """
        render renders the UI-Element onto the given surface

        Args:
            surface (Surface): the surface the UIElement should be drawn on
        """
        assert self._drawer is not None

        if self._core.getCurrentToggleState():
            self.__fillBox.render(surface)
            self.__fillCross[0].render(surface)
            self.__fillCross[1].render(surface)

from typing import Any, Callable, override

from ......utility   import Rect
from ......display   import Surface
from .....createinfo import CreateInfo
from ....atoms       import AtomCreateOption, Box, Line
from ..interactable  import Interactable

from .buttoncore         import ButtonCore
from .buttondata         import ButtonData
from .buttoncreateoption import ButtonCO
from .buttonprefab       import ButtonPrefab

class Button(Interactable[ButtonCore, ButtonData, ButtonCO, ButtonPrefab]):

    __fillBox: Box
    __fillCross: tuple[Line, Line]

    # -------------------- creation --------------------

    def __init__(self, rect: Rect, buttonActive: bool=True,
                 renderData: ButtonPrefab | list[ButtonCO | AtomCreateOption] | ButtonData=ButtonPrefab.BASIC, active: bool = True) -> None:
        assert self._renderstyle is not None

        if isinstance(renderData, list):
            myData: ButtonData = ButtonData()
            for createOption in renderData:
                myData += (createOption, self._renderstyle)
            myData += (ButtonCO.CREATE, self._renderstyle)
            renderData = myData
        elif isinstance(renderData, ButtonPrefab):
            renderData = ButtonData() * (renderData, self._renderstyle)

        super().__init__(ButtonCore(rect, buttonActive), renderData, active)

        self.__fillBox   = self._renderData.fillData.createElement(rect)
        self.__fillCross = (self._renderData.crossData[0].createElement(rect),
                            self._renderData.crossData[1].createElement(rect))
        self.__fillBox.alignpoint(self)
        self.__fillBox.alignpoint(self, (1,1),(1,1), keepSize=False)
        self.__fillCross[0].alignpoint(self)
        self.__fillCross[0].alignpoint(self, (1,1),(1,1), keepSize=False)
        self.__fillCross[1].alignpoint(self)
        self.__fillCross[1].alignpoint(self, (1,1),(1,1), keepSize=False)
    
    @staticmethod
    @override
    def fromCreateOptions(createOptions: list[ButtonCO]) -> CreateInfo['Button']:
        """
        fromCreateOptions creates the element from createoptions.

        Args:
            createoptions (list[CreateOption]): the list of create-options to be used for creating

        Returns (creator for this class): createinfo for this class
        """
        return CreateInfo(Button, renderData=createOptions)

    @staticmethod
    @override
    def fromPrefab(prefab: ButtonPrefab) -> CreateInfo['Button']:
        """
        fromPrefab creates the element from a prefab.

        Args:
            prefab (Prefab): the prefab to be created

        Returns (creator for this class): createinfo for this class
        """
        return CreateInfo(Button, renderData=prefab)

    # -------------------- subscriptions --------------------

    def subscribeToClick(self, callback: str) -> bool:
        """
        subscribeToClick subscribes a Callback to the Event of the object
        getting clicked.

        Args:
            callback (str): the id of the callback to subscribe to the click

        Returns (bool): returns if the subscription was successful
        """
        return self._core.subscribeToClick(callback)
    
    def unsubscribeToClick(self, callback: str) -> bool:
        """
        unsubscribeToClick unsubscribes a callback (by id) from the Event of the
        object getting clicked.

        Args:
            callback (str): the id of the callback to unsubscribe

        Returns (bool): if the unsubscription was successful
        """
        return self._core.unsubscribeToClick(callback)

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

        if self._core.isPressed():
            self.__fillBox.render(surface)
            self.__fillCross[0].render(surface)
            self.__fillCross[1].render(surface)

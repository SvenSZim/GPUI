from typing import Any, Callable, override

from ......utility   import Rect
from ......display   import Surface
from .....createinfo import CreateInfo
from ....atoms       import AtomCreateOption, Box, Line
from ..interactable  import Interactable

from .slidercore         import SliderCore
from .sliderdata         import SliderData
from .slidercreateoption import SliderCO
from .sliderprefab       import SliderPrefab

class Slider(Interactable[SliderCore, SliderData, SliderCO, SliderPrefab]):

    __fillBox: Box
    __fillLine: Line

    # -------------------- creation --------------------

    def __init__(self, rect: Rect, sliderStart: float=0.5, horizontalSlider: bool=True, sliderActive: bool=True,
                 renderData: SliderPrefab | list[SliderCO | AtomCreateOption] | SliderData=SliderPrefab.BASIC, active: bool = True) -> None:
        assert self._renderstyle is not None

        if isinstance(renderData, list):
            myData: SliderData = SliderData()
            for createOption in renderData:
                myData += (createOption, self._renderstyle)
            myData += (SliderCO.CREATE, self._renderstyle)
            renderData = myData
        elif isinstance(renderData, SliderPrefab):
            renderData = SliderData() * (renderData, self._renderstyle)

        super().__init__(SliderCore(rect, sliderStartState=sliderStart, horizontalSlider=horizontalSlider, sliderActive=sliderActive), renderData, active)

        self.__fillBox = self._renderData.fillData.createElement(rect)
        self.__fillLine = self._renderData.lineData.createElement(rect)
        self.__fillBox.alignpoint(self)
        if horizontalSlider:
            self.__fillBox.alignaxis(self, 3)
            self.__fillLine.alignpoint(self, otherPoint=(0.0, 0.5))
        else:
            self.__fillBox.alignaxis(self, 1)
            self.__fillLine.alignpoint(self, otherPoint=(0.5, 0.0))
    
    @staticmethod
    @override
    def fromCreateOptions(createOptions: list[SliderCO]) -> CreateInfo['Slider']:
        """
        fromCreateOptions creates the element from createoptions.

        Args:
            createoptions (list[CreateOption]): the list of create-options to be used for creating

        Returns (creator for this class): createinfo for this class
        """
        return CreateInfo(Slider, renderData=createOptions)

    @staticmethod
    @override
    def fromPrefab(prefab: SliderPrefab) -> CreateInfo['Slider']:
        """
        fromPrefab creates the element from a prefab.

        Args:
            prefab (Prefab): the prefab to be created

        Returns (creator for this class): createinfo for this class
        """
        return CreateInfo(Slider, renderData=prefab)

    # -------------------- getter --------------------

    def getSliderState(self) -> float:
        """
        getSliderState returns the current slider state
        (activation state between 0 and 1)
        """
        return self._core.getSliderState()

    # -------------------- subscriptions --------------------

    def subscribeToHold(self, callback: str) -> bool:
        """
        subscribeToHold subscribes a Callback to the Event of the slider
        getting pressed down.

        Args:
            callback (str): the id of the callback to subscribe to the click

        Returns (bool): returns if the subscription was successful
        """
        return self._core.subscribeToHold(callback)
    
    def unsubscribeToHold(self, callback: str) -> bool:
        """
        unsubscribeToHold unsubscribes a callback (by id) from the Event of the
        slider getting pressed down.

        Args:
            callback (str): the id of the callback to unsubscribe

        Returns (bool): if the unsubscription was successful
        """
        return self._core.unsubscribeToHold(callback)

    def quickSubscribeToHold(self, f: Callable, *args: Any) -> tuple[str, bool]:
        """
        quickSubscribeToHold takes a function and its arguments, creates
        a Callback and subscribes to the Event of the slider getting pressed down.

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

        if not self._active:
            return

        if self._core.isHorizontalSlider():
            self.__fillBox.setWidth(int(self.getWidth() * self._core.getSliderState()))
        else:
            self.__fillBox.setHeight(int(self.getHeight() * self._core.getSliderState()))
        if self._core.isHorizontalSlider():
            self.__fillLine.setWidth(int(self.getWidth() * self._core.getSliderState()))
        else:
            self.__fillLine.setHeight(int(self.getHeight() * self._core.getSliderState()))

        self.__fillBox.render(surface)
        self.__fillLine.render(surface)

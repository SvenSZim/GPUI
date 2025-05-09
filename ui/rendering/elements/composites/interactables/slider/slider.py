from typing import Any, Callable, override

from ......utility   import Rect, AlignType
from ......display   import Surface
from ....atoms       import AtomCreateOption, Box, Line
from ..interactable  import Interactable

from .slidercore         import SliderCore
from .sliderdata         import SliderData
from .slidercreateoption import SliderCO
from .sliderprefab       import SliderPrefab

class Slider(Interactable[SliderCore, SliderData, SliderCO, SliderPrefab]):

    __prevRenderState: float

    __fillBox: Box
    __fillLine: Line

    # -------------------- creation --------------------

    def __init__(self, rect: Rect, sliderStart: float=0.5, horizontalSlider: bool=True, sliderActive: bool=True,
                 renderData: SliderPrefab | list[SliderCO | AtomCreateOption] | SliderData=SliderPrefab.BASIC, active: bool = True) -> None:
        assert self._renderstyle is not None

        self.__prevRenderState = 0.0

        if isinstance(renderData, list):
            myData: SliderData = SliderData()
            for createOption in renderData:
                myData += (createOption, self._renderstyle)
            myData += (SliderCO.CREATE, self._renderstyle)
            renderData = myData
        elif isinstance(renderData, SliderPrefab):
            renderData = SliderData() * (renderData, self._renderstyle)

        super().__init__(SliderCore(rect, sliderStartState=sliderStart, horizontalSlider=horizontalSlider, sliderActive=sliderActive), renderData, active)

        self.__fillBox = Box(Rect(), renderData=self._renderData.fillData)
        self.__fillLine = Line(Rect(), renderData=self._renderData.lineData)
        self.__fillBox.align(self)
        if horizontalSlider:
            self.__fillBox.alignSize(self, alignX=False)
            self.__fillLine.align(self, AlignType.iMiL)
        else:
            self.__fillBox.alignSize(self, alignY=False)
            self.__fillLine.align(self, AlignType.iTiM)
    
    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'Slider':
        return Slider(Rect())

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

        if self.__prevRenderState != self._core.getSliderState():
            if self._core.isHorizontalSlider():
                size: int = int(self.getWidth() * self._core.getSliderState())
                self.__fillBox.alignSize(Rect(size=(size, 0)), alignY=False)
                self.__fillLine.alignSize(Rect(size=(size, 0)), alignY=False)
            else:
                size: int = int(self.getHeight() * self._core.getSliderState())
                self.__fillBox.alignSize(Rect(size=(0, size)), alignX=False)
                self.__fillLine.alignSize(Rect(size=(0, size)), alignX=False)
            self.__fillBox._core._body.forceUpdate()
            self.__fillLine._core._body.forceUpdate()
            self.__prevRenderState = self._core.getSliderState()

        self.__fillBox.render(surface)
        self.__fillLine.render(surface)

from typing import Any, Callable, override

from ......utility  import Rect
from ......display  import Surface
from ......interaction  import InputEvent, InputManager
from ..interactable import Interactable

from .slidercore    import SliderCore
from .sliderdata    import SliderData

class Slider(Interactable[SliderCore, SliderData]):

    __prevRenderState: float

    # -------------------- creation --------------------

    def __init__(self, rect: Rect, renderData: SliderData, sliderStart: float=0.5, horizontalSlider: bool=True, sliderActive: bool=True, active: bool = True) -> None:
        self.__prevRenderState = -1.0

        super().__init__(SliderCore(rect, sliderStartState=sliderStart, horizontalSlider=horizontalSlider, sliderActive=sliderActive), renderData, active)
        self._renderData.alignInner(self, horizontalSlider)
    
    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'Slider':
        slider: Slider = Slider(Rect(), SliderData.parseFromArgs(args))
        hasTrigger: bool = False
        for tag, value in args.items():
            match tag:
                case 'trigger':
                    hasTrigger = True
                    for v in Slider.parseList(value):
                        if v.lower() == 'click':
                            slider._core.addTriggerEvent(InputManager.getEvent(InputEvent.LEFTDOWN))
                            slider._core.addReleaseEvent(InputManager.getEvent(InputEvent.LEFTUP))
                        else:
                            slider._core.addTriggerEvent(InputManager.getEvent(InputEvent.fromStr(value)))
                            slider._core.addReleaseEvent(InputManager.getEvent(InputEvent(InputEvent.fromStr(value).value+1)))
                case 'globaltrigger' | 'gtrigger' | 'global':
                    hasTrigger = True
                    for v in Slider.parseList(value):
                        if v.lower() == 'click':
                            slider._core.addGlobalTriggerEvent(InputManager.getEvent(InputEvent.LEFTDOWN))
                            slider._core.addReleaseEvent(InputManager.getEvent(InputEvent.LEFTUP))
                        else:
                            slider._core.addGlobalTriggerEvent(InputManager.getEvent(InputEvent.fromStr(value)))
                            slider._core.addReleaseEvent(InputManager.getEvent(InputEvent(InputEvent.fromStr(value).value+1)))
        if not hasTrigger:
            slider._core.addTriggerEvent(InputManager.getEvent(InputEvent.LEFTDOWN))
            slider._core.addReleaseEvent(InputManager.getEvent(InputEvent.LEFTUP))
        return slider

    # -------------------- access-point --------------------

    @override
    def set(self, args: dict[str, Any], sets: int=-1, maxDepth: int=-1) -> int:
        """
        set is a general access point to an element. It has some basic functionality implemented and is overridden
        by some elements for more specific behavior (updating text in Text, subscribing to buttonpresses in button, etc.).
        set also recursivly applies the given args to all children until the given amount of
        'sets' or the maxDepth is reached. A 'set' is counted, if any of the given args can be applied to the element.

        Returns (int): the amount of 'sets' applied
        """
        super().set(args)
        for tag, value in args.items():
            match tag:
                case 'subscribeToHold':
                    if isinstance(value, str):
                        self._core.subscribeToHold(value)
                    else:
                        raise ValueError('subscribeToHold expects a callbackID')
                case 'unsubscribeToHold':
                    if isinstance(value, str):
                        self._core.unsubscribeToHold(value)
                    else:
                        raise ValueError('unsubscribeToHold expects a callbackID')
                case 'quickSubscribeToHold':
                    if isinstance(value, tuple) and isinstance(value[0], Callable) and isinstance(value[1], list):
                        self._core.quickSubscribeToHold(value[0], *value[1])
                    else:
                        raise ValueError('quickSubscribeToHold expects a 2-tuple with a Callable and a list of arguments')
                case 'getSliderState':
                    if isinstance(value, Callable):
                        value(self._core.getSliderState())
                    else:
                        raise ValueError('getSliderState expects a callable with one float parameter to write the slider-state to')

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
                self._renderData.fillData.alignSize(Rect(size=(size, 0)), alignY=False)
                self._renderData.lineData.alignSize(Rect(size=(size, 0)), alignY=False)
            else:
                size: int = int(self.getHeight() * self._core.getSliderState())
                self._renderData.fillData.alignSize(Rect(size=(0, size)), alignX=False)
                self._renderData.lineData.alignSize(Rect(size=(0, size)), alignX=False)
            self._renderData.fillData.forceUpdate()
            self._renderData.lineData.forceUpdate()
            self.__prevRenderState = self._core.getSliderState()

        self._renderData.fillData.render(surface)
        self._renderData.lineData.render(surface)

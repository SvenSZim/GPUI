from typing import Any, override

from ......utility      import Rect
from ......interaction  import EventManager, InputManager, Holdable
from ..interactablecore import InteractableCore

class SliderCore(InteractableCore, Holdable):
    """
    SliderCore is the core object of the interactable 'Slider'.
    """
    __updateSliderCallback: str

    __sliderState: float
    __horizontalSlider: bool

    def __init__(self, rect: Rect, sliderStartState: float=0.5, horizontalSlider: bool=True, sliderActive: bool=True) -> None:
        InteractableCore.__init__(self, rect)
        Holdable.__init__(self, sliderActive)
        self.__sliderState = sliderStartState
        self.__horizontalSlider = horizontalSlider

        self.__updateSliderCallback = EventManager.createCallback(self._updateSlider)
        self.subscribeToHold(self.__updateSliderCallback)

    @override
    def getInnerSizing(self, elSize: tuple[int, int], args: dict[str, Any]) -> tuple[int, int]:
        return elSize

    def getSliderState(self) -> float:
        return self.__sliderState

    def isHorizontalSlider(self) -> bool:
        return self.__horizontalSlider

    def _updateSlider(self) -> None:
        if not self._buttonActive:
            return
        mousepos: tuple[int, int] = InputManager.getMousePosition()
        if self.__horizontalSlider:
            if self.getWidth() != 0:
                self.__sliderState = min(1.0, max(0.0, (mousepos[0] - self.getLeft()) / self.getWidth()))
        else:
            if self.getHeight() != 0:
                self.__sliderState = min(1.0, max(0.0, (mousepos[1] - self.getTop()) / self.getHeight()))

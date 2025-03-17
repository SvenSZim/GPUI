from typing import Any, Callable, Optional, override

from ...generic import Rect, Color
from ...uidrawerinterface import UISurface

from ..uiobject import UIObject
from ..UIABC import UIABC
from .UIButtonCore import UIButtonCore
from .UISButton import UISButton
from .UISButtonCreateOptions import UISButtonCreateOptions
from .UIButtonRenderData import UIButtonRenderData
from .UISButtonCreator import UISButtonCreator
from .UISButtonPrefabs import UISButtonPrefabs


class UIButton(UIABC[UIButtonCore, UIButtonRenderData]):
    """
    UIButtonRender is the UIElementRender for all UIButtons.
    """

    def __init__(self, core: UIButtonCore, active: bool=True, renderStyleData: UISButton | list[UISButtonCreateOptions] | UIButtonRenderData=UISButton.BASIC) -> None:
        """
        __init__ initializes the UIButtonRender instance

        Args:
            core: UIButton | UIABCBody | Rect = the refering UIButton (Or UIABCBody bcs. they are 'equivalet')
            active: bool = active-state of the UIButtonRenderer
            renderStyleElement: UIStyledButtons = the render style that should be used when rendering styled
        """
        assert self._renderstyle is not None

        if isinstance(renderStyleData, UISButton):
            renderStyleData = UISButtonPrefabs.getPrefabRenderData(renderStyleData, self._renderstyle)
        elif isinstance(renderStyleData, list):
            renderStyleData = UISButtonCreator.createStyledElement(renderStyleData, self._renderstyle)
        
        super().__init__(core, active, renderStyleData)

    def addButtonTriggerEvent(self, event: str) -> bool:
        return self._core.addTriggerEvent(event)

    def addGlobalButtonTriggerEvent(self, event: str) -> bool:
        return self._core.addGlobalTriggerEvent(event)

    def subscribeToButtonEvent(self, state: int, f: Callable, *args: Any) -> bool:
        return self._core.subscribeToButtonEvent(state, f, *args)

    def subscribeToButtonClick(self, f: Callable, *args: Any) -> bool:
        return self._core.subscribeToButtonClick(f, *args)


    
    @override
    def render(self, surface: UISurface) -> None:
        """
        render renders the UIButton onto the given surface

        Args:
            surface: UISurface = the surface the UIButton should be drawn on
        """
        assert self._drawer is not None

        rect: Rect = self._core.getBody().getRect()
        numberOfStates: int = self._core.getNumberOfButtonStates()
        currentState: int = self._core.getCurrentButtonState()
        stateColor: Optional[Color] = self._renderData.stateDispColor

        # check if UIElement should be rendered
        if not self._active:
            return

        # draw object
        drawObject: UIObject = UIObject(rect, renderStyleData=self._renderData.objectData)

        drawObject.renderFill(surface)

        if stateColor is not None:
            match self._renderData.stateDispStyle:
                case 1:
                    activation_percent: float = currentState / (numberOfStates - 1)
                    activation_width: int = int(rect.width * activation_percent)
                    self._drawer.drawrect(surface, Rect(rect.getPosition(), (activation_width, rect.height)), stateColor)


        drawObject.renderBorders(surface)

        

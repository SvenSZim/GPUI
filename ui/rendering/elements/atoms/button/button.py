from typing import Any, Callable, override

from ....utility import Rect
from ....display import Surface

from ..atom               import Atom
from .buttoncore          import ButtonCore
from .buttondata          import ButtonData
from .buttoncreateoption  import ButtonCO
from .buttoncreator       import ButtonCreator
from .buttonprefab        import ButtonPrefab
from .buttonprefabmanager import ButtonPrefabManager


class Button(Atom[ButtonCore, ButtonData, ButtonCO, ButtonPrefab]):
    """
    Button is a simple ui-atom-element for drawing a button.
    """

    def __init__(self, rect: Rect, numberOfStates: int=2, startState: int=0, active: bool=True, 
                 renderStyleData: ButtonPrefab | list[ButtonCO] | ButtonData=ButtonPrefab.BASIC) -> None:
        assert self._renderstyle is not None

        if isinstance(renderStyleData, list):
            renderStyleData = ButtonCreator.createButtonData(renderStyleData, self._renderstyle)
        elif isinstance(renderStyleData, ButtonPrefab):
            renderStyleData = ButtonPrefabManager.createButtonData(renderStyleData, self._renderstyle)

        super().__init__(ButtonCore(rect, numberOfStates, startState), active, renderStyleData)

    @staticmethod
    @override
    def constructor(rect: Rect, active: bool=True, renderStyleData: ButtonPrefab | list[ButtonCO] | ButtonData=ButtonPrefab.BASIC) -> 'Button':
        return Button(rect, active=active, renderStyleData=renderStyleData)

    @staticmethod
    @override
    def fromCreateOptions(createOptions: list[ButtonCO]) -> 'Button':
        """
        fromCreateOptions creates the atom-element from createoptions.

        Args:
            createoptions (list[CreateOption]): the list of create-options to be used for creating

        Returns (this class): instance of the created atom
        """
        return Button(Rect(), renderStyleData=createOptions)

    @staticmethod
    @override
    def fromPrefab(prefab: ButtonPrefab) -> 'Button':
        """
        fromPrefab creates the atom-element from a prefab.

        Args:
            prefab (Prefab): the prefab to be created

        Returns (this class): instance of the created atom
        """
        return Button(Rect(), renderStyleData=prefab)

    def addButtonTriggerEvent(self, event: str) -> bool:
        return self._core.addTriggerEvent(event)

    def addGlobalButtonTriggerEvent(self, event: str) -> bool:
        return self._core.addGlobalTriggerEvent(event)

    def subscribeToButtonEvent(self, state: int, f: Callable, *args: Any) -> bool:
        return self._core.subscribeToButtonEvent(state, f, *args)

    def subscribeToButtonClick(self, f: Callable, *args: Any) -> bool:
        return self._core.subscribeToButtonClick(f, *args)


    @override
    def render(self, surface: Surface) -> None:
        """
        render renders the Button onto the given surface

        Args:
            surface: Surface = the surface the Button should be drawn on
        """
        assert self._drawer is not None

        rect: Rect = self._core.getBody().getRect()
        numberOfStates: int = self._core.getNumberOfButtonStates()
        currentState: int = self._core.getCurrentButtonState()

        # check if Element should be rendered
        if not self._active:
            return

        if self._renderData.stateDispColor is not None:
            match self._renderData.stateDispStyle:
                case 1:
                    activation_percent: float = currentState / (numberOfStates - 1)
                    activation_width: int = int(rect.width * activation_percent)
                    self._drawer.drawrect(surface, Rect(rect.getPosition(), (activation_width, rect.height)), self._renderData.stateDispColor)
        

from typing import Any, Callable, override

from ....utility import Rect
from ....display import Surface

from ..atom               import Atom
from .togglecore          import ToggleCore
from .toggledata          import ToggleData
from .togglecreateoption  import ToggleCO
from .togglecreator       import ToggleCreator
from .toggleprefab        import TogglePrefab
from .toggleprefabmanager import TogglePrefabManager


class Toggle(Atom[ToggleCore, ToggleData, ToggleCO, TogglePrefab]):
    """
    Toggle is a simple ui-atom-element for drawing a toggle.
    """

    # -------------------- creation --------------------

    def __init__(self, rect: Rect, numberOfStates: int=2, startState: int=0, active: bool=True, 
                 renderStyleData: TogglePrefab | list[ToggleCO] | ToggleData=TogglePrefab.BASIC) -> None:
        assert self._renderstyle is not None

        if isinstance(renderStyleData, list):
            renderStyleData = ToggleCreator.createToggleData(renderStyleData, self._renderstyle)
        elif isinstance(renderStyleData, TogglePrefab):
            renderStyleData = TogglePrefabManager.createToggleData(renderStyleData, self._renderstyle)

        super().__init__(ToggleCore(rect, numberOfStates, startState), active, renderStyleData)

    @staticmethod
    @override
    def constructor(rect: Rect, active: bool=True, renderStyleData: TogglePrefab | list[ToggleCO] | ToggleData=TogglePrefab.BASIC) -> 'Toggle':
        return Toggle(rect, active=active, renderStyleData=renderStyleData)

    @staticmethod
    @override
    def fromCreateOptions(createOptions: list[ToggleCO]) -> 'Toggle':
        """
        fromCreateOptions creates the atom-element from createoptions.

        Args:
            createoptions (list[CreateOption]): the list of create-options to be used for creating

        Returns (this class): instance of the created atom
        """
        return Toggle(Rect(), renderStyleData=createOptions)

    @staticmethod
    @override
    def fromPrefab(prefab: TogglePrefab) -> 'Toggle':
        """
        fromPrefab creates the atom-element from a prefab.

        Args:
            prefab (Prefab): the prefab to be created

        Returns (this class): instance of the created atom
        """
        return Toggle(Rect(), renderStyleData=prefab)

    # -------------------- interactive --------------------

    def addTriggerEvent(self, event: str) -> bool:
        return self._core.addTriggerEvent(event)

    def addGlobalTriggerEvent(self, event: str) -> bool:
        return self._core.addGlobalTriggerEvent(event)

    def subscribeToClick(self, f: Callable, *args: Any) -> bool:
        return self._core.subscribeToClick(f, *args)

    def subscribeToToggleState(self, state: int, f: Callable, *args: Any) -> bool:
        return self._core.subscribeToToggleState(state, f, *args)

    # -------------------- rendering --------------------

    @override
    def render(self, surface: Surface) -> None:
        """
        render renders the Toggle onto the given surface

        Args:
            surface: Surface = the surface the Toggle should be drawn on
        """
        assert self._drawer is not None

        rect: Rect = self._core.getBody().getRect()
        numberOfStates: int = self._core.getNumberOfToggleStates()
        currentState: int = self._core.getCurrentToggleState()

        # check if Element should be rendered
        if not self._active:
            return

        if self._renderData.stateDispColor is not None:
            match self._renderData.stateDispStyle:
                case 1:
                    activation_percent: float = currentState / (numberOfStates - 1)
                    activation_width: int = int(rect.width * activation_percent)
                    self._drawer.drawrect(surface, Rect(rect.getPosition(), (activation_width, rect.height)), self._renderData.stateDispColor)
        

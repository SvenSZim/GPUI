from typing import Callable

from ....style   import RenderStyle, StyleManager
from .toggledata   import ToggleData
from .toggleprefab import TogglePrefab

class TogglePrefabManager:
    """
    TogglePrefabManager is an intern class for storing the maps from
    the TogglePrefab's to the ToggleData for rendering.
    """
    __prefabs: dict[TogglePrefab, Callable[[RenderStyle], ToggleData]] = {
        TogglePrefab.INVISIBLE       : lambda _     : ToggleData(),
        TogglePrefab.BASIC           : lambda style : ToggleData(stateDispStyle=1, stateDispColor=StyleManager.getStyleColor(0, style)),
        TogglePrefab.BASIC_ALT       : lambda style : ToggleData(stateDispStyle=1, stateDispColor=StyleManager.getStyleColor(1, style)),
    }
    
    @staticmethod
    def createToggleData(prefab: TogglePrefab, style: RenderStyle) -> ToggleData:
        """
        createToggleData creates a ToggleData object from a given prefab with a given style.

        Args:
            prefab (TogglePrefab) : the prefab to be used
            style  (RenderStyle): the style to be used

        Returns (ToggleData): the RenderData created from the given args
        """
        if TogglePrefabManager.__prefabs.get(prefab):
            return TogglePrefabManager.__prefabs[prefab](style)
        raise ValueError(f'TogglePrefab::{prefab=} does not exist')


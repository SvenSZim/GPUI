from typing import Callable

from ....style   import RenderStyle, StyleManager
from .buttondata   import ButtonData
from .buttonprefab import ButtonPrefab

class ButtonPrefabManager:
    """
    ButtonPrefabManager is an intern class for storing the maps from
    the ButtonPrefab's to the ButtonData for rendering.
    """
    __prefabs: dict[ButtonPrefab, Callable[[RenderStyle], ButtonData]] = {
        ButtonPrefab.INVISIBLE       : lambda _     : ButtonData(),
        ButtonPrefab.BASIC           : lambda style : ButtonData(stateDispStyle=1, stateDispColor=StyleManager.getStyleColor(0, style)),
        ButtonPrefab.BASIC_ALT       : lambda style : ButtonData(stateDispStyle=1, stateDispColor=StyleManager.getStyleColor(1, style)),
    }
    
    @staticmethod
    def createButtonData(prefab: ButtonPrefab, style: RenderStyle) -> ButtonData:
        """
        createButtonData creates a ButtonData object from a given prefab with a given style.

        Args:
            prefab (ButtonPrefab) : the prefab to be used
            style  (RenderStyle): the style to be used

        Returns (ButtonData): the RenderData created from the given args
        """
        if ButtonPrefabManager.__prefabs.get(prefab):
            return ButtonPrefabManager.__prefabs[prefab](style)
        raise ValueError(f'ButtonPrefab::{prefab=} does not exist')


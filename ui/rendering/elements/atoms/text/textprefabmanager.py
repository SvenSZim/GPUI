from typing import Callable

from ....style   import RenderStyle, StyleManager
from .textdata   import TextData
from .textprefab import TextPrefab

class TextPrefabManager:
    """
    TextPrefabManager is an intern class for storing the maps from
    the TextPrefab's to the TextData for rendering.
    """

    # #################### CLASS-METHODS ####################

    __prefabs: dict[TextPrefab, Callable[[RenderStyle], TextData]] = {
        TextPrefab.BASIC           : lambda style : TextData(textColor=StyleManager.getStyleColor(0, style)),
        TextPrefab.DYNAMIC_BASIC   : lambda style : TextData(dynamicText=True, textColor=StyleManager.getStyleColor(0, style)),
    }
    
    @staticmethod
    def createTextData(prefab: TextPrefab, style: RenderStyle) -> TextData:
        """
        createTextData creates a TextData object from a given prefab with a given style.

        Args:
            prefab (TextPrefab) : the prefab to be used
            style  (RenderStyle): the style to be used

        Returns (TextData): the RenderData created from the given args
        """
        if TextPrefabManager.__prefabs.get(prefab):
            return TextPrefabManager.__prefabs[prefab](style)
        raise ValueError(f'TextPrefab::{prefab=} does not exist')


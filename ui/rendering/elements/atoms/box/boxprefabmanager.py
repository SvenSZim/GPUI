from typing import Callable

from ....style   import RenderStyle, StyleManager
from .boxdata   import BoxData
from .boxprefab import BoxPrefab


class BoxPrefabManager:
    """
    BoxPrefabManager is an intern class for storing the maps from
    the BoxPrefab's to the BoxData for rendering.
    """

    __prefabs: dict[BoxPrefab, Callable[[RenderStyle], BoxData]] = {
        BoxPrefab.INVISIBLE     : lambda _     : BoxData(),
        BoxPrefab.BASIC         : lambda style : BoxData(fillColor=StyleManager.getStyleColor(0, style)),
        BoxPrefab.ALTCOLOR      : lambda style : BoxData(fillColor=StyleManager.getStyleColor(1, style))
    }
    
    @staticmethod
    def createBoxData(prefab: BoxPrefab, style: RenderStyle) -> BoxData:
        """
        createBoxData creates a BoxData object from a given prefab with a given style.

        Args:
            prefab (BoxPrefab) : the prefab to be used
            style  (RenderStyle): the style to be used

        Returns (BoxData): the RenderData created from the given args
        """
        if BoxPrefabManager.__prefabs.get(prefab):
            return BoxPrefabManager.__prefabs[prefab](style)
        raise ValueError(f'BoxPrefab::{prefab=} does not exist')


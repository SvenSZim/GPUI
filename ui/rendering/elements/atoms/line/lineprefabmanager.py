from typing import Callable

from ....style   import RenderStyle, StyleManager
from .linedata   import LineData
from .lineprefab import LinePrefab

class LinePrefabManager:
    """
    LinePrefabManager is an intern class for storing the maps from
    the LinePrefab's to the LineData for rendering.
    """

    __prefabs: dict[LinePrefab, Callable[[RenderStyle], LineData]] = {
        LinePrefab.INVISIBLE   : lambda _     : LineData(),
        LinePrefab.SOLID       : lambda style : LineData(StyleManager.getStyleColor(0, style)),
        LinePrefab.DOTTED      : lambda style : LineData(StyleManager.getStyleColor(0, style), doAlt=True, altAbsLen=10.0),
        LinePrefab.ALTERNATING : lambda style : LineData(StyleManager.getStyleColor(0, style), doAlt=True, altAbsLen=10.0, altColor=StyleManager.getStyleColor(1, style)),
        LinePrefab.SHRINKED    : lambda style : LineData(StyleManager.getStyleColor(0, style), partial=0.75),
        LinePrefab.SHRINKED_DOTTED:lambda style : LineData(StyleManager.getStyleColor(0, style), partial=0.75, doAlt=True, altAbsLen=10.0),
    }
    
    @staticmethod
    def createLineData(prefab: LinePrefab, style: RenderStyle) -> LineData:
        """
        createLineData creates a LineData object from a given prefab with a given style.

        Args:
            prefab (LinePrefab) : the prefab to be used
            style  (RenderStyle): the style to be used

        Returns (LineData): the RenderData created from the given args
        """
        if LinePrefabManager.__prefabs.get(prefab):
            return LinePrefabManager.__prefabs[prefab](style)
        raise ValueError(f'LinePrefabManager::{prefab=} does not exist')


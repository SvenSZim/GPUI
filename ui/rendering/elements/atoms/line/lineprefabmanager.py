from typing import Callable

from ....style   import RenderStyle, StyleManager
from .linedata   import LineData
from .lineprefab import LinePrefab

class LinePrefabManager:

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
        if LinePrefabManager.__prefabs.get(prefab):
            return LinePrefabManager.__prefabs[prefab](style)
        raise ValueError(f'LinePrefabManager::{prefab=} does not exist')


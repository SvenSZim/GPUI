from typing import Callable

from ....style   import RenderStyle, StyleManager
from ..line import LinePrefab
from .boxdata   import BoxData
from .boxprefab import BoxPrefab


class BoxPrefabManager:
    """
    BoxPrefabManager is an intern class for storing the maps from
    the BoxPrefab's to the BoxData for rendering.
    """

    __prefabs: dict[BoxPrefab, Callable[[RenderStyle], BoxData]] = {
        BoxPrefab.INVISIBLE     : lambda _     : BoxData(borderData=LinePrefab.INVISIBLE),
        BoxPrefab.BORDERONLY    : lambda _     : BoxData(borderData=LinePrefab.SOLID, doBorders=(True, True, True, True)),
        BoxPrefab.BORDER_DOTTED : lambda _     : BoxData(borderData=LinePrefab.DOTTED, doBorders=(True, True, True, True)),
        BoxPrefab.BORDER_SHRINKED : lambda _   : BoxData(borderData=LinePrefab.SHRINKED, doBorders=(True, True, True, True)),
        BoxPrefab.BORDER_SHRINKED_DOTTED : lambda _ : BoxData(borderData=LinePrefab.SHRINKED_DOTTED, doBorders=(True, True, True, True)),
        BoxPrefab.SOLID         : lambda style : BoxData(borderData=LinePrefab.SOLID, fillColor=StyleManager.getStyleColor(0, style)),
        BoxPrefab.BORDER_TB     : lambda _     : BoxData(borderData=LinePrefab.SOLID, doBorders=(True, False, False, True)),
        BoxPrefab.BASIC         : lambda _     : BoxData(borderData=LinePrefab.SOLID, doBorders=(True, True, True, True))
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


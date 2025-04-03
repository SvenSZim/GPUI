from typing import override

from .....utility import Rect
from .....display import Surface

from ....createinfo    import CreateInfo
from ..atom            import Atom
from .boxcore          import BoxCore
from .boxdata          import BoxData
from .boxcreateoption  import BoxCO
from .boxprefab        import BoxPrefab

class Box(Atom[BoxCore, BoxData, BoxCO, BoxPrefab]):
    """
    Box is a simple ui-atom-element for drawing a box.
    """

    # -------------------- creation --------------------

    def __init__(self, rect: Rect, renderData: BoxPrefab | list[BoxCO] | BoxData=BoxPrefab.BASIC, active: bool=True) -> None:
        assert self._renderstyle is not None

        if isinstance(renderData, list):
            myData: BoxData = BoxData()
            for createOption in renderData:
                myData += (createOption, self._renderstyle)
            renderData = myData
        elif isinstance(renderData, BoxPrefab):
            renderData = BoxData() * (renderData, self._renderstyle)

        assert isinstance(renderData, BoxData)
        super().__init__(BoxCore(rect), renderData, active)

    @staticmethod
    @override
    def fromCreateOptions(createOptions: list[BoxCO]) -> CreateInfo['Box']:
        """
        fromCreateOptions creates the atom-element from createoptions.

        Args:
            createoptions (list[CreateOption]): the list of create-options to be used for creating

        Returns (creator for this class): createinfo for this class
        """
        return CreateInfo(Box, renderData=createOptions)

    @staticmethod
    @override
    def fromPrefab(prefab: BoxPrefab) -> CreateInfo['Box']:
        """
        fromPrefab creates the atom-element from a prefab.

        Args:
            prefab (Prefab): the prefab to be created

        Returns (creator for this class): createinfo for this class
        """
        return CreateInfo(Box, renderData=prefab)

    # -------------------- rendering --------------------

    @override
    def render(self, surface: Surface) -> None:
        """
        render renders the Box onto the given surface

        Args:
            surface: Surface = the surface the Box should be drawn on
        """
        assert self._drawer is not None
        rect: Rect = self.getRect()
        
        if not self._active or (rect.width == 0 and rect.height == 0):
            return
        
        # render fill color
        if self._renderData.fillColor is not None:
            self._drawer.drawrect(surface, rect, self._renderData.fillColor)

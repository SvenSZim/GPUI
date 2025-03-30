from typing import override

from ....utility import Rect
from ....display import Surface

from ..atom            import Atom
from .boxcore          import BoxCore
from .boxdata          import BoxData
from .boxcreateoption  import BoxCO
from .boxcreator       import BoxCreator
from .boxprefab        import BoxPrefab
from .boxprefabmanager import BoxPrefabManager

class Box(Atom[BoxCore, BoxData, BoxCO, BoxPrefab]):
    """
    Box is a simple ui-atom-element for drawing a box.
    """

    def __init__(self, rect: Rect, active: bool=True, renderStyleData: BoxPrefab | list[BoxCO] | BoxData=BoxPrefab.BASIC) -> None:
        assert self._renderstyle is not None

        if isinstance(renderStyleData, list):
            renderStyleData = BoxCreator.createBoxData(renderStyleData, self._renderstyle)
        elif isinstance(renderStyleData, BoxPrefab):
            renderStyleData = BoxPrefabManager.createBoxData(renderStyleData, self._renderstyle)

        assert isinstance(renderStyleData, BoxData)
        super().__init__(BoxCore(rect), active, renderStyleData)

    @staticmethod
    @override
    def constructor(rect: Rect, active: bool=True, renderStyleData: BoxPrefab | list[BoxCO] | BoxData=BoxPrefab.BASIC) -> 'Box':
        return Box(rect, active=active, renderStyleData=renderStyleData)

    @staticmethod
    @override
    def fromCreateOptions(createOptions: list[BoxCO]) -> 'Box':
        """
        fromCreateOptions creates the atom-element from createoptions.

        Args:
            createoptions (list[CreateOption]): the list of create-options to be used for creating

        Returns (this class): instance of the created atom
        """
        return Box(Rect(), renderStyleData=createOptions)

    @staticmethod
    @override
    def fromPrefab(prefab: BoxPrefab) -> 'Box':
        """
        fromPrefab creates the atom-element from a prefab.

        Args:
            prefab (Prefab): the prefab to be created

        Returns (this class): instance of the created atom
        """
        return Box(Rect(), renderStyleData=prefab)

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

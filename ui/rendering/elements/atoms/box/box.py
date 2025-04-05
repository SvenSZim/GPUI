from typing import override
from numpy  import sqrt

from .....utility import Rect
from .....display import Surface

from ....createinfo    import CreateInfo
from ..atom            import Atom
from .boxcore          import BoxCore
from .boxdata          import BoxData, AltMode
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

        if rect.width < 0:
            rect = Rect((rect.left + rect.width, rect.top), (-rect.width, rect.height))
        if rect.height < 0:
            rect = Rect((rect.left, rect.top + rect.height), (rect.width, -rect.height))
        inset: int = int(min(rect.width, rect.height) * (1.0 - self._renderData.partial) / 2)
        rect = Rect((rect.left + inset, rect.top + inset),
                    (rect.width - 2 * inset, rect.height - 2 * inset))
        
        match self._renderData.altMode:
            case AltMode.CHECKERBOARD:
                assert self._renderData.altAbsLen is not None
                stepLength: float = self._renderData.altAbsLen
                start_rect: Rect = Rect(rect.getPosition(), (int(stepLength), int(stepLength)))
                rowStartFirstColor: bool = True
                while start_rect.bottom < rect.bottom:
                    firstColor: bool = rowStartFirstColor
                    while start_rect.right < rect.right:
                        if firstColor:
                            if self._renderData.mainColor is not None:
                                self._drawer.drawrect(surface, start_rect, self._renderData.mainColor)
                        else:
                            if self._renderData.altColor is not None:
                                self._drawer.drawrect(surface, start_rect, self._renderData.altColor)
                        firstColor = not firstColor
                        start_rect = Rect((start_rect.right, start_rect.top), (int(stepLength), int(stepLength)))
                    if firstColor:
                        if self._renderData.mainColor is not None:
                            self._drawer.drawrect(surface, Rect((start_rect.left, start_rect.top), (rect.right - start_rect.left, int(stepLength))), self._renderData.mainColor)
                    else:
                        if self._renderData.altColor is not None:
                            self._drawer.drawrect(surface, Rect((start_rect.left, start_rect.top), (rect.right - start_rect.left, int(stepLength))), self._renderData.altColor)
                    rowStartFirstColor = not rowStartFirstColor
                    start_rect = Rect((rect.left, start_rect.bottom), (int(stepLength), int(stepLength)))
                missing_height: int = rect.bottom - start_rect.top
                start_rect = Rect(start_rect.getPosition(), (int(stepLength), missing_height))
                while start_rect.right < rect.right:
                    if rowStartFirstColor:
                        if self._renderData.mainColor is not None:
                            self._drawer.drawrect(surface, start_rect, self._renderData.mainColor)
                    else:
                        if self._renderData.altColor is not None:
                            self._drawer.drawrect(surface, start_rect, self._renderData.altColor)
                    rowStartFirstColor = not rowStartFirstColor
                    start_rect = Rect((start_rect.right, start_rect.top), (int(stepLength), missing_height))
                if rowStartFirstColor:
                    if self._renderData.mainColor is not None:
                        self._drawer.drawrect(surface, Rect((start_rect.left, start_rect.top), (rect.right - start_rect.left, missing_height)), self._renderData.mainColor)
                else:
                    if self._renderData.altColor is not None:
                        self._drawer.drawrect(surface, Rect((start_rect.left, start_rect.top), (rect.right - start_rect.left, missing_height)), self._renderData.altColor)

            case _:
                if self._renderData.mainColor is not None:
                    self._drawer.drawrect(surface, rect, self._renderData.mainColor)

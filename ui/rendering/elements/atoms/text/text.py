from typing import override

from .....utility import Rect
from .....display import Surface, Font, FontManager

from ..atom             import Atom
from .textcore          import TextCore
from .textdata          import TextData
from .textcreateoption  import TextCO
from .textcreator       import TextCreator
from .textprefab        import TextPrefab
from .textprefabmanager import TextPrefabManager


class Text(Atom[TextCore, TextData, TextCO, TextPrefab]):
    """
    Text is a simple ui-atom-element for drawing a text.
    """

    # -------------------- creation --------------------

    def __init__(self, rect: Rect, content: str, active: bool=True, renderStyleData: TextPrefab | list[TextCO] | TextData=TextPrefab.BASIC) -> None:
        assert self._renderstyle is not None
        
        if isinstance(renderStyleData, list):
            renderStyleData = TextCreator.createTextData(renderStyleData, self._renderstyle)
        elif isinstance(renderStyleData, TextPrefab):
            renderStyleData = TextPrefabManager.createTextData(renderStyleData, self._renderstyle)


        assert isinstance(renderStyleData, TextData)
        super().__init__(TextCore(rect, content), active, renderStyleData)
        self.updateContent(self._core.getContent())

    @staticmethod
    @override
    def constructor(rect: Rect, content: str, active: bool=True, renderStyleData: TextPrefab | list[TextCO] | TextData=TextPrefab.BASIC) -> 'Text':
        return Text(rect, content, active=active, renderStyleData=renderStyleData)

    @staticmethod
    @override
    def fromCreateOptions(createOptions: list[TextCO]) -> 'Text':
        """
        fromCreateOptions creates the atom-element from createoptions.

        Args:
            createoptions (list[CreateOption]): the list of create-options to be used for creating

        Returns (this class): instance of the created atom
        """
        return Text(Rect(), '', renderStyleData=createOptions)

    @staticmethod
    @override
    def fromPrefab(prefab: TextPrefab) -> 'Text':
        """
        fromPrefab creates the atom-element from a prefab.

        Args:
            prefab (Prefab): the prefab to be created

        Returns (this class): instance of the created atom
        """
        return Text(Rect(), '', renderStyleData=prefab)

    # -------------------- content-modification --------------------

    def updateContent(self, content: str) -> None:
        self._core.setContent(content)
        if self._renderData.dynamicText:
            self._renderData.fontSize = getDynamicFontSize(self._renderData.sysFontName, self._core.getBody().getRect().getSize(), content)

    # -------------------- rendering --------------------

    @override
    def render(self, surface: Surface) -> None:
        """
        render renders the UIText onto the given surface

        Args:
            surface (Surface): the surface the UIText should be drawn on
        """
        assert self._drawer is not None

        rect: Rect = self.getRect()

        # check if UIElement should be rendered
        if not self._active:
            return

        if self._renderData.textColor is not None and self._renderData.fontSize is not None:
                
            font: Font = FontManager.getFont().SysFont(self._renderData.sysFontName, self._renderData.fontSize)
            text_render: Surface = font.render(self._core.getContent(), self._renderData.textColor)
            text_size: tuple[int, int] = text_render.getSize()
            text_position: tuple[int, int] = (int(rect.getPosition()[0] + (rect.getSize()[0] - text_size[0]) / 2),
                                                  int(rect.getPosition()[1] + (rect.getSize()[1] - text_size[1]) / 2))
            surface.blit(text_render, text_position)


# -------------------------------------------------- helpers --------------------------------------------------

def getDynamicFontSize(font_name: str, box_size: tuple[int, int], text: str) -> int:
    """
    getDynamicFont calculates the maximal fontsize to use for the given SysFont
    to still make the given text fit in the given box

    Args:
        font_name: str = the SysFont name to use
        box_size: tuple[int, int]: the size of the box the text should fit in
        text: str = the text to fit in the box

    Returns:
        int = the maximal fontsize to still fit in the box
    """

    def text_fits_in_box(text_render: Surface) -> bool:
        nonlocal box_size
        text_size: tuple[int, int] = text_render.getSize()
        return (box_size[0] > text_size[0]) and (box_size[1] > text_size[1])

    start_search: int = 0
    end_search: int = min(box_size)
    while start_search < end_search:
        mid_search: int = int((start_search + end_search) / 2)
        
        test_font = FontManager.getFont().SysFont(font_name, mid_search)
        test_render: Surface = test_font.render(text, (255, 255, 255))

        if text_fits_in_box(test_render):
            start_search = mid_search + 1
        else: 
            end_search = mid_search - 1

    return start_search

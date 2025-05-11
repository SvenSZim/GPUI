from typing import Optional, override

from .....utility import Rect
from .....display import Surface, Font, FontManager
from .....interaction import EventManager

from ...body        import Body
from ..atom             import Atom
from .textcore          import TextCore
from .textdata          import TextData, fontSizeFunction
from .textcreateoption  import TextCO
from .textprefab        import TextPrefab


class Text(Atom[TextCore, TextData, TextCO, TextPrefab]):
    """
    Text is a simple ui-atom-element for drawing a text.
    """

    # -------------------- creation --------------------

    def __init__(self, rect: Rect, content: str, renderData: TextPrefab | list[TextCO] | TextData=TextPrefab.BASIC, active: bool=True) -> None:
        assert self._renderstyle is not None
        
        if isinstance(renderData, list):
            myData: TextData = TextData()
            for createOption in renderData:
                myData += (createOption, self._renderstyle)
            renderData = myData
        elif isinstance(renderData, TextPrefab):
            renderData = TextData() * (renderData, self._renderstyle)


        assert isinstance(renderData, TextData)
        super().__init__(TextCore(rect, content), renderData, active)

        self.__renderCache = None
        EventManager.quickSubscribe(Body.getLayoutUpdateEvent(), self.updateRenderData)

    @staticmethod
    @override
    def parseFromArgs(args: dict[str, str]) -> 'Text':
        data: TextData = TextData()
        for arg, value in args.items():
            match arg:
                case 'inset':
                    data.inset = Text.parsePartial(value)
                case 'color':
                    data.textColor = value
                case 'fontsize':
                    if 'd' in value:
                        data.dynamicText = True
                    else:
                        sizeconv: dict[str, int] = {x:i for i, x in enumerate(['xxs','xs','s','ms','sm','m','lm','ml','l','xl','xxl'])}
                        if value.lower() in sizeconv:
                            data.fontSize = fontSizeFunction(sizeconv[value.lower()])
                        else:
                            data.fontSize = int(Text.extractNum(value))
                case 'fontname':
                    data.sysFontName = value
                case 'align':
                    if ',' in value:
                        xx, yy = 0.5, 0.5
                        x, y = [v.strip() for v in value.split(',')][:2]
                        if '.' in x:
                            vk, nk = [Text.extractNum(v) for v in x.split('.')][:2]
                            xx = int(vk) + int(nk)/10**len(nk)
                        else:
                            match x.lower()[0]:
                                case 'l':
                                    xx = 0.0
                                case 'r':
                                    xx = 1.0
                        if '.' in y:
                            vk, nk = [Text.extractNum(v) for v in y.split('.')][:2]
                            yy = int(vk) + int(nk)/10**len(nk)
                        else:
                            match y.lower()[0]:
                                case 't':
                                    yy = 0.0
                                case 'b':
                                    yy = 1.0
                        data.fontAlign = (xx, yy)
                    else:
                        xx = 0.5
                        x = value.strip()
                        if '.' in x:
                            vk, nk = [Text.extractNum(v) for v in x.split('.')][:2]
                            xx = int(vk) + int(nk)/10**len(nk)
                        else:
                            match x.lower()[0]:
                                case 'l':
                                    xx = 0.0
                                case 'r':
                                    xx = 1.0
                        data.fontAlign = (xx, xx)
        return Text(Rect(), args['content'], renderData=data)

    # -------------------- content-modification --------------------

    def updateContent(self, content: str) -> None:
        self._core.setContent(content)
        if self._renderData.dynamicText:
            self._renderData.fontSize = getDynamicFontSize(self._renderData.sysFontName, self._core.getBody().getRect().getSize(), content)

    # -------------------- rendering --------------------

    __renderCache: Optional[tuple[Surface, tuple[int, int]]]

    def updateRenderData(self) -> None:
        self.__renderCache = None
        #calculate render borderbox
        rect: Rect = self.getRect()

        #check for errors in boxsize
        if rect.isZero():
            return
        if rect.width < 0:
            rect = Rect((rect.left + rect.width, rect.top), (-rect.width, rect.height))
        if rect.height < 0:
            rect = Rect((rect.left, rect.top + rect.height), (rect.width, -rect.height))
        
        #apply partialInset
        def applyPartial(rect: Rect, partialInset: tuple[float, float] | float | tuple[int, int] | int) -> Rect:
            if isinstance(partialInset, tuple):
                if isinstance(partialInset[0], float):
                    rect = Rect((rect.left + int(rect.width * (1.0 - partialInset[0])),
                                 rect.top + int(rect.height * (1.0 - partialInset[1]))),
                                (int(rect.width * (1.0 - 2 * partialInset[0])), int(rect.height * (1.0 - 2 * partialInset[1]))))
                else:
                    assert isinstance(partialInset[1], int)
                    rect = Rect((rect.left + partialInset[0], rect.top + partialInset[1]), (rect.width - 2 * partialInset[0], rect.height - 2 * partialInset[1]))
            elif isinstance(partialInset, float):
                inset: int = int(min(rect.width, rect.height) * partialInset)
                rect = Rect((rect.left + inset, rect.top + inset),
                            (rect.width - 2 * inset, rect.height - 2 * inset))
            else:
                rect = Rect((rect.left + partialInset, rect.top + partialInset), (rect.width - 2 * partialInset, rect.height - 2 * partialInset))
            return rect
        
        globalInset: tuple[float, float] | float | tuple[int, int] | int = self._renderData.inset
        rect = applyPartial(rect, globalInset)
        if rect.isZero():
            return

        if self._renderData.dynamicText:
            self._renderData.fontSize = getDynamicFontSize(self._renderData.sysFontName, rect.getSize(), self._core.getContent())

        if self._renderData.textColor is not None and self._renderData.fontSize is not None:
            font: Font = FontManager.getFont().SysFont(self._renderData.sysFontName, self._renderData.fontSize)
            text_render: Surface = font.render(self._core.getContent(), self._renderData.textColor)
            text_size: tuple[int, int] = text_render.getSize()
            textPosX: int = int(rect.left + (rect.width - text_size[0]) * self._renderData.fontAlign[0])
            textPosY: int = int(rect.top + (rect.height - text_size[1]) * self._renderData.fontAlign[1])
            self.__renderCache = (text_render, (textPosX, textPosY))


    @override
    def render(self, surface: Surface) -> None:
        """
        render renders the UIText onto the given surface

        Args:
            surface (Surface): the surface the UIText should be drawn on
        """
        assert self._drawer is not None

        # check if UIElement should be rendered
        if self._active and self.__renderCache is not None:
            surface.blit(self.__renderCache[0], self.__renderCache[1])

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

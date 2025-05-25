from typing import Any, Optional, override

from .....display   import Surface
from ...element     import Element
from ...atoms       import Text

from .sectioncore         import SectionCore
from .sectiondata         import SectionData

class Section(Element[SectionCore, SectionData]):

    # -------------------- creation --------------------

    def __init__(self, renderData: SectionData, header: Optional[tuple[Element, float]], footer: Optional[tuple[Element, float]],
                 *inner: tuple[Element, float], innerLimit: float=5.0, offset: int=0, active: bool = True) -> None:
        super().__init__(SectionCore(header, footer, *inner, innerLimit=innerLimit, offset=offset), renderData, active)
        self._renderData.alignInner(self._core.getVBox(), (header[1]/self._core.getTotalRelHeight() if header is not None else 0.0,
                                                           footer[1]/self._core.getTotalRelHeight() if footer is not None else 0.0))
    
    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'Section':
        inner: list[Element] = args['inner']
        offset = 0
        sizings: list[float] = [1.0 for _ in inner]
        limit: int = 5
        for arg, v in args.items():
            match arg.lower():
                case 'offset' | 'spacing':
                    offset = int(Section.extractNum(v))
                case 'size' | 'sizes' | 'sizing' | 'sizings':
                    sizings = list(map(Section.parseNum, Section.adjustList(list(map(str, sizings)), Section.parseList(v))))

                case 'limit' | 'innerlimit' | 'inneramount':
                    limit = int(Section.extractNum(v))
        return Section(SectionData.parseFromArgs({}), (Text.parseFromArgs({'content':'Cool Section', 'fontsize':'d', 'col':'white'}), 2.0),
                       (Text.parseFromArgs({'content':'Cool Footer', 'col':'red'}), 0.5), *zip(inner, sizings), innerLimit=limit, offset=offset)

    # -------------------- active-state --------------------

    @override
    def setActive(self, active: bool) -> None:
        super().setActive(active)
        self._core.setActive(active)

    @override
    def toggleActive(self) -> bool:
        bb = super().toggleActive()
        self._core.setActive(bb)
        return bb

    # -------------------- rendering --------------------

    @override
    def render(self, surface: Surface) -> None:
        """
        render renders the UI-Element onto the given surface

        Args:
            surface (Surface): the surface the UIElement should be drawn on
        """
        assert self._drawer is not None
        
        if not self._active:
            return

        # inner element
        header: Optional[Element] = self._core.getHeader()
        footer: Optional[Element] = self._core.getFooter()
        if footer is not None:
            footer.render(surface)
        for el in self._core.getInner():
            el.render(surface)
        for btn in self._core.getButtons():
            btn.render(surface)
        if header is not None:
            header.render(surface)

        # separators
        self._renderData.borderData[0].render(surface)
        self._renderData.borderData[1].render(surface)

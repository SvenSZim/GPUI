from typing import Any, Optional, override

from ......display   import Surface
from ....element     import Element
from ..addon         import Addon

from .sectioncore         import SectionCore
from .sectiondata         import SectionData

class Section(Addon[SectionCore, SectionData]):

    # -------------------- creation --------------------

    def __init__(self, inner: Element, renderData: SectionData, header: Optional[Element]=None, footer: Optional[Element]=None, offset: int=0, active: bool = True) -> None:
        super().__init__(SectionCore(inner, header, footer, offset=offset), renderData, active)
        self._renderData.alignInner(self, offset)
    
    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'Section':
        return Section(args['inner'], SectionData.parseFromArgs(args))

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
        self._core.getInner().render(surface)
        if header is not None:
            header.render(surface)

        # separators
        self._renderData.borderData[0].render(surface)
        self._renderData.borderData[1].render(surface)

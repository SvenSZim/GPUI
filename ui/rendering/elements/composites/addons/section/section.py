from typing import Any, Optional, override

from ......utility   import Rect, AlignType
from ......display   import Surface
from ....element     import Element
from ....atoms       import AtomCreateOption, Line
from ..addon         import Addon

from .sectioncore         import SectionCore
from .sectiondata         import SectionData
from .sectioncreateoption import SectionCO
from .sectionprefab       import SectionPrefab

class Section(Addon[Element, SectionCore, SectionData, SectionCO, SectionPrefab]):

    __headerseparator: Line
    __footerseparator: Line

    # -------------------- creation --------------------

    def __init__(self, inner: Element, header: Optional[Element]=None, footer: Optional[Element]=None, offset: int=0,
                 renderData: SectionPrefab | list[SectionCO | AtomCreateOption] | SectionData=SectionPrefab.BASIC, active: bool = True) -> None:
        assert self._renderstyle is not None

        if isinstance(renderData, list):
            myData: SectionData = SectionData()
            for createOption in renderData:
                myData += (createOption, self._renderstyle)
            renderData = myData
        elif isinstance(renderData, SectionPrefab):
            renderData = SectionData() * (renderData, self._renderstyle)

        super().__init__(SectionCore(inner, header, footer, offset=offset), renderData, active)

        self.__headerseparator = Line(Rect(), renderData=self._renderData.borderData[0])
        self.__footerseparator = Line(Rect(), renderData=self._renderData.borderData[1])
        self.__headerseparator.align(self._core.getInner(), AlignType.iTM, offset=(0, -offset//2))
        self.__headerseparator.alignSize(self._core.getInner(), alignY=False)
        self.__footerseparator.align(self._core.getInner(), AlignType.iBM, offset=(0, offset//2))
        self.__footerseparator.alignSize(self._core.getInner(), alignY=False)
    
    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'Section':
        return Section(args['inner'])

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
        self.__headerseparator.render(surface)
        self.__footerseparator.render(surface)

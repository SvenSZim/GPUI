from typing import Optional, override

from ......utility   import Rect
from ......display   import Surface
from .....createinfo import CreateInfo
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
            myData += (SectionCO.CREATE, self._renderstyle)
            renderData = myData
        elif isinstance(renderData, SectionPrefab):
            renderData = SectionData() * (renderData, self._renderstyle)

        super().__init__(SectionCore(inner, header, footer, offset=offset), renderData, active)

        self.__headerseparator = self._renderData.borderData[0].createElement(Rect())
        self.__footerseparator = self._renderData.borderData[1].createElement(Rect())
        self.__headerseparator.alignpoint(self._core.getInner(), offset=(0, -offset//2))
        self.__headerseparator.alignpoint(self._core.getInner(), (1,1),(1,0), offset=(0, -offset//2), keepSize=False)
        self.__footerseparator.alignpoint(self._core.getInner(), otherPoint=(0,1), offset=(0, offset//2))
        self.__footerseparator.alignpoint(self._core.getInner(), (1,1),(1,1), offset=(0, offset//2), keepSize=False)
    
    @staticmethod
    @override
    def fromCreateOptions(createOptions: list[SectionCO]) -> CreateInfo['Section']:
        """
        fromCreateOptions creates the element from createoptions.

        Args:
            createoptions (list[CreateOption]): the list of create-options to be used for creating

        Returns (creator for this class): createinfo for this class
        """
        return CreateInfo(Section, renderData=createOptions)

    @staticmethod
    @override
    def fromPrefab(prefab: SectionPrefab) -> CreateInfo['Section']:
        """
        fromPrefab creates the element from a prefab.

        Args:
            prefab (Prefab): the prefab to be created

        Returns (creator for this class): createinfo for this class
        """
        return CreateInfo(Section, renderData=prefab)

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

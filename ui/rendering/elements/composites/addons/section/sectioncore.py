from typing import Optional, override

from ......utility import Rect
from ....element   import Element
from ..addoncore   import AddonCore

class SectionCore(AddonCore[Element]):
    """
    SectionCore is the core object of the addon 'Section'.
    """
    __header: Optional[Element]
    __footer: Optional[Element]
    __offset: int

    def __init__(self, inner: Element, header: Optional[Element], footer: Optional[Element], offset: int=0) -> None:
        self.__header = header
        self.__footer = footer
        self.__offset = offset

        width: int = inner.getWidth()
        height: int = inner.getHeight()
        if header is not None:
            if header.getWidth() > width:
                width = header.getWidth()
            height += header.getHeight() + offset
        if footer is not None:
            if footer.getWidth() > width:
                width = footer.getWidth()
            height += footer.getHeight() + offset

        super().__init__(Rect(size=(width, height)), inner)

    def getHeader(self) -> Optional[Element]:
        return self.__header

    def getFooter(self) -> Optional[Element]:
        return self.__footer

    @override
    def _alignInner(self) -> None:
        totalHeight: int = self._inner.getHeight()
        if self.__header is not None:
            totalHeight += self.__header.getHeight() + self.__offset
        if self.__footer is not None:
            totalHeight += self.__footer.getHeight() + self.__offset
        totalHeight = max(totalHeight, 1)

        topOffset: int = 0
        if self.__header is not None:
            self.__header.alignpoint(self)
            topOffset += self.__header.getHeight()
            self.__header.alignpoint(self, (1,1), (1, topOffset/totalHeight), keepSize=False)
            topOffset += self.__offset

        self._inner.alignpoint(self, otherPoint=(0, topOffset/totalHeight))
        topOffset += self._inner.getHeight()
        self._inner.alignpoint(self, (1,1), (1, topOffset/totalHeight), keepSize=False)
        topOffset += self.__offset

        if self.__footer is not None:
            self.__footer.alignpoint(self, otherPoint=(0, topOffset/totalHeight))
            self.__footer.alignpoint(self, (1,1), (1,1), keepSize=False)

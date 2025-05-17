from typing import Any, override

from ......utility   import AlignType
from ......display   import Surface
from ....element     import Element
from ....atoms       import Box, Line
from ..addon         import Addon

from .framedcore         import FramedCore
from .frameddata         import FramedData
from .framedcreateoption import FramedCO
from .framedprefab       import FramedPrefab

class Framed(Addon[Element, FramedCore, FramedData, FramedCO, FramedPrefab]):

    __background: Box
    __borders: tuple[Line, Line, Line, Line]

    # -------------------- creation --------------------

    def __init__(self, inner: Element, renderData: tuple[tuple[Line, Line, Line, Line], Box], offset: int=0, active: bool = True) -> None:
        assert self._renderstyle is not None

        super().__init__(FramedCore(inner, offset=offset), FramedData(), active)

        self.__borders, self.__background = renderData
        
        self.__background.align(self)
        self.__background.alignSize(self)
        self.__borders[0].align(self)
        self.__borders[0].align(self, AlignType.iBL, keepSize=False)
        self.__borders[1].align(self, AlignType.iTiR)
        self.__borders[1].align(self, AlignType.iBR, keepSize=False)
        self.__borders[2].align(self)
        self.__borders[2].align(self, AlignType.TiR, keepSize=False)
        self.__borders[3].align(self, AlignType.iBiL)
        self.__borders[3].align(self, AlignType.BiR, keepSize=False)
    
    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'Framed':
        offset: int = 0
        for arg, v in args.items():
            match arg:
                case 'offset' | 'padding' | 'inset':
                    offset = int(Framed.extractNum(v))
        return Framed(args['inner'], ((args['border0'], args['border1'], args['border2'], args['border3']), args['fill']), offset=offset)

    # -------------------- rendering --------------------

    @override
    def render(self, surface: Surface) -> None:
        """
        render renders the UI-Element onto the given surface

        Args:
            surface (Surface): the surface the UIElement should be drawn on
        """
        assert self._drawer is not None
        
        # background
        self.__background.render(surface)

        # inner element
        self._core.getInner().render(surface)

        # outlines
        for border in self.__borders:
            border.render(surface)

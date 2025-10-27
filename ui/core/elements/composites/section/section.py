from typing import Any, Optional, override

from .....utility import StyledDefault
from .....display   import Surface
from ...element     import Element
from ...atoms       import Box

from .sectioncore         import SectionCore
from .sectiondata         import SectionData

class Section(Element[SectionCore, SectionData]):
    """A sectioned container element that organizes content into paginated views.
    
    The Section composite provides a container that can split its content into
    multiple pages when it exceeds a specified height limit. It supports:
    - Optional header and footer elements
    - Automatic content pagination
    - Navigation buttons for section traversal
    - Section separators between header/content/footer
    - Keyboard navigation (left/right arrows)
    
    The content is automatically split into sections based on the innerLimit parameter,
    with navigation controls appearing when multiple sections are created.
    """

    # -------------------- creation --------------------

    def __init__(self, header: Optional[tuple[Element, float]], footer: Optional[tuple[Element, float]], inner: list[tuple[Element, float]],
                 separators: tuple[Optional[Element], Optional[Element]]=(None, None), innerLimit: float=5.0, offset: int=0, active: bool = True) -> None:
        btn1: Optional[Element] = Section.getStyledElement(StyledDefault.BUTTON_TXT)
        btn2: Optional[Element] = Section.getStyledElement(StyledDefault.BUTTON_TXT)
        if btn1 is None:
            btn1 = Box.parseFromArgs({})
        if btn2 is None:
            btn2 = Box.parseFromArgs({})
        super().__init__(SectionCore(header, footer, (btn1, btn2), inner, separators=separators, innerLimit=innerLimit, offset=offset), SectionData(), active)
 
    @staticmethod
    @override
    def getMinRequiredChildren() -> int:
        return 1

    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'Section':
        inner: list[Element] = args['inner']
        offset = 0
        sizings: list[float] = [1.0 for _ in inner]
        limit: float = 5.0
        useheader: bool = False
        usefooter: bool = False
        for arg, v in args.items():
            match arg.lower():
                case 'offset' | 'spacing':
                    offset = int(Section.extractNum(v))
                case 'size' | 'sizes' | 'sizing' | 'sizings':
                    sizings = list(map(Section.parseNum, Section.adjustList(list(map(str, sizings)), Section.parseList(v))))

                case 'limit' | 'innerlimit' | 'inneramount':
                    limit = float(Section.parseNum(v))
                case 'header':
                    useheader = True
                case 'footer':
                    usefooter = True
        if len(inner) == 1:
            return Section(None, None, list(zip(inner, sizings)), innerLimit=limit, offset=offset)
        if useheader and usefooter and len(inner) > 2:
            separators = (Section.getStyledElement(StyledDefault.BORDER), Section.getStyledElement(StyledDefault.BORDER))
            return Section((inner[0], sizings[0]), (inner[1], sizings[1]), list(zip(inner[2:], sizings[2:])), separators=separators, innerLimit=limit, offset=offset)
        elif useheader:
            separators = (Section.getStyledElement(StyledDefault.BORDER), None)
            return Section((inner[0], sizings[0]), None, list(zip(inner[1:], sizings[1:])), separators=separators, innerLimit=limit, offset=offset)
        elif usefooter:
            separators = (None, Section.getStyledElement(StyledDefault.BORDER))
            return Section(None, (inner[0], sizings[0]), list(zip(inner[1:], sizings[1:])), separators=separators, innerLimit=limit, offset=offset)
        return Section(None, None, list(zip(inner, sizings)), innerLimit=limit, offset=offset)


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

    # -------------------- access-point --------------------

    @override
    def _set(self, args: dict[str, Any], sets: int = -1, maxDepth: int = -1, skips: bool = False) -> bool:
        s: bool = super()._set(args, sets, maxDepth, skips)
        for tag, value in args.items():
            match tag.lower():
                case 'setInnerLimit' | 'setLimit' | 'limit':
                    s = True
                    if isinstance(value, float) or isinstance(value, int):
                        self._core.setInnerLimit(float(value))
                    else:
                        raise ValueError('setInnerLimit expects a float or int')
        return s

    @override
    def set(self, args: dict[str, Any], sets: int = -1, maxDepth: int = -1, skips: list[int] = [0]) -> int:
        return int(self._set(args, sets, maxDepth, bool(skips[0])))

    # -------------------- rendering --------------------

    @override
    def setZIndex(self, zindex: int) -> None:
        super().setZIndex(zindex)
        for el in self._core.getInner():
            el.setZIndex(zindex)
        for btn in self._core.getButtons():
            btn.setZIndex(zindex+5)
        hd, ft = self._core.getHeader(), self._core.getFooter()
        if hd:
            hd.setZIndex(zindex+2)
        if ft:
            ft.setZIndex(zindex+1)

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
        for el in self._core.getCurrentSectionElements():
            el.render(surface)
        if header is not None:
            header.render(surface)
        for btn in self._core.getButtons():
            btn.render(surface)

        # separators
        headsep: Optional[Element]
        footsep: Optional[Element]
        headsep, footsep = self._core.getSeparators()
        if headsep:
            headsep.render(surface)
        if footsep:
            footsep.render(surface)


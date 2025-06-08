from typing import Any, override

from .....utility   import AlignType, iRect, Rect
from .....display   import Surface
from ...element     import Element

from .uicore        import UICore
from .uidata        import UIData

class UI(Element[UICore, UIData]):

    __namedElements: dict[str, Element]

    # -------------------- creation --------------------

    def __init__(self, namedElements: dict[str, Element], core: UICore, active: bool = True) -> None:
        super().__init__(core, UIData(), active)
        self.__namedElements = namedElements
    
    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'UI':
        inner: list[Element] = args['inner']
        named: dict[str, Element] = args['named']
        offset = 0
        sizing = 1.0
        useheader: bool = False
        usefooter: bool = False
        for arg, v in args.items():
            match arg.lower():
                case 'offset' | 'spacing':
                    offset = int(UI.extractNum(v))
                case 'size' | 'sizing' | 'relativesize' | 'relsize':
                    sizing = UI.parseNum(v)

                case 'header':
                    useheader = True
                case 'footer':
                    usefooter = True
        return UI(named, UICore(useheader, usefooter, inner, offset=offset, sizing=sizing))
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

    def getElementByID(self, id: str) -> Element:
        if id in self.__namedElements:
            return self.__namedElements[id]
        raise ValueError(f'{id=} does not exist')

    @override
    def set(self, args: dict[str, Any], sets: int = -1, maxDepth: int = -1, skips: list[int] = [0]) -> int:
        return int(self._set(args, sets, maxDepth, bool(skips[0])))

    # -------------------- aligning --------------------

    def setPosition(self, position: tuple[int, int]) -> None:
        """
        setPosition sets the position of the ui

        Args:
            position (tuple[int, int]): the position to set the ui to
        """
        self.align(Rect(topleft=position))

    @override
    def align(self, other: 'Element | iRect', align: AlignType = AlignType.iTiL, alignX: bool = True, alignY: bool = True, offset: int | tuple[int, int] = 0, keepSize: bool = True) -> None:
        super().align(other, align, alignX, alignY, offset, keepSize)
        self.updateLayout()
        self._core.alignInner()
        self.updateLayout()

    def setSize(self, size: tuple[int, int]) -> None:
        """
        setSize sets the size of the ui

        Args:
            size (tuple[int, int]): the size to set the ui to
        """
        self.alignSize(Rect(size=size))

    @override
    def alignSize(self, other: 'Element | iRect', alignX: bool = True, alignY: bool = True, relativeAlign: float | tuple[float, float] = 1.0, absoluteOffset: int | tuple[int, int] = 0) -> None:
        super().alignSize(other, alignX, alignY, relativeAlign, absoluteOffset)
        self.updateLayout()
        self._core.alignInner()
        self.updateLayout()

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

        for el in self._core.getCurrentElements():
            el.render(surface)
        
        if len(UI._postRenderQueue) > 0:
            UI._renderPost(surface)

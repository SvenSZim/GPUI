from typing import Any, Callable, override

from ......interaction  import InputEvent, InputManager
from ......display      import Surface
from ....element        import Element
from ..addon            import Addon

from .dropdowncore         import DropdownCore
from .dropdowndata         import DropdownData

class Dropdown(Addon[DropdownCore, DropdownData]):

    # -------------------- creation --------------------

    def __init__(self, head: Element, renderData: DropdownData | dict[str, Any], dropdownActive: bool=True, active: bool = True) -> None:
        if isinstance(renderData, dict):
            renderData = DropdownData.parseFromArgs(renderData)
        Addon.__init__(self, DropdownCore(head, buttonActive=dropdownActive), renderData, active)

        self._renderData.alignInner(self)
        self._core.quickSubscribeToToggleState(0, self._renderData.dropdown.setActive, False)
        self._core.quickSubscribeToToggleState(1, self._renderData.dropdown.setActive, True)

    @override
    def setActive(self, active: bool) -> None:
        super().setActive(active)
        self._renderData.dropdown.setActive(active and bool(self._core.getCurrentToggleState()))

    @override
    def toggleActive(self) -> bool:
        bb = super().toggleActive()
        self.setActive(bb)
        return bb

    @staticmethod
    @override
    def getMinRequiredChildren() -> int:
        return 1

    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'Dropdown':
        inner: list[Element] = args['inner']
        dpd = Dropdown(inner[0], DropdownData.parseFromArgs(args))
        dpd._core.adjustFromArgs(args, hasTrigger=False)
        return dpd

    # -------------------- access-point --------------------

    @override
    def set(self, args: dict[str, Any], sets: int=-1, maxDepth: int=-1) -> int:
        """
        set is a general access point to an element. It has some basic functionality implemented and is overridden
        by some elements for more specific behavior (updating text in Text, subscribing to buttonpresses in button, etc.).
        set also recursivly applies the given args to all children until the given amount of
        'sets' or the maxDepth is reached. A 'set' is counted, if any of the given args can be applied to the element.

        Returns (int): the amount of 'sets' applied
        """
        s: int = super().set(args, sets, maxDepth)
        s |= int(self._core.set(args))
        s |= int(self._renderData.set(args))
        if 0 <= maxDepth < 2:
            return s
        if sets < 0 or s < sets:
            s += self._core.setinner(args, sets-s, maxDepth-1)
        if sets < 0 or s < sets:
            s += self._renderData.setinner(args, sets-s, maxDepth-1)
        return s

    # -------------------- rendering --------------------

    @override
    def render(self, surface: Surface) -> None:
        """
        render renders the UI-Element onto the given surface

        Args:
            surface (Surface): the surface the UIElement should be drawn on
        """
        assert self._drawer is not None

        if self._active:
            self._core.getInner().render(surface)

            if self._core.getCurrentToggleState():
                self.addPostRenderElement(self._renderData.dropdown)

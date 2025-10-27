from typing import Any, override

from ......display      import Surface
from ....element        import Element
from ..addon            import Addon

from .dropdowncore         import DropdownCore
from .dropdowndata         import DropdownData

class Dropdown(Addon[DropdownCore, DropdownData]):
    """An addon that adds collapsible dropdown functionality to an element.
    
    Wraps a header element with dropdown behavior that:
    - Shows/hides a dropdown panel on interaction
    - Manages dropdown panel positioning
    - Handles z-index layering for proper overlap
    - Controls dropdown state and animations
    
    Commonly used to create dropdown menus, expandable panels,
    or any interface element that needs to show/hide content
    based on user interaction.
    """

    # -------------------- creation --------------------

    def __init__(self, head: Element, renderData: DropdownData, dropdownActive: bool=True, active: bool = True) -> None:
        Addon.__init__(self, DropdownCore(head, renderData.dropdown, buttonActive=dropdownActive), renderData, active)

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
    def _set(self, args: dict[str, Any], sets: int = -1, maxDepth: int = -1, skips: bool = False) -> bool:
        s: bool = super()._set(args, sets, maxDepth, skips)
        s |= self._core.set(args, skips)
        s |= self._renderData.set(args, skips)
        return s

    @override
    def set(self, args: dict[str, Any], sets: int = -1, maxDepth: int = -1, skips: list[int]=[0]) -> int:
        """
        set is a general access point to an element. It has some basic functionality implemented and is overridden
        by some elements for more specific behavior (updating text in Text, subscribing to buttonpresses in button, etc.).
        set also recursivly applies the given args to all children until the given amount of
        'sets' or the maxDepth is reached. A 'set' is counted, if any of the given args can be applied to the element.

        Returns (int): the amount of 'sets' applied
        """
        ts: int = 0
        s: bool = self._set(args, sets, maxDepth, bool(skips[0]))
        ts += int(s and not skips[0])
        if 0 <= maxDepth < 2:
            return ts
        skips[0] = max(0, skips[0]-ts)
        if sets < 0 or ts < sets:
            cs: int = self._core.setinner(args, sets-ts, maxDepth-1, skips)
            skips[0] = max(0, skips[0]-cs)
            ts += cs
        if sets < 0 or ts < sets:
            cs: int = self._renderData.setinner(args, sets-ts, maxDepth-1, skips)
            skips[0] = max(0, skips[0]-cs)
            ts += cs
        return ts

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

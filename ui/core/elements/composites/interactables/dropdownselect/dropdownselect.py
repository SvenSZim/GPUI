from typing import Any, Callable, Optional, override

from ......utility      import StyledDefault
from ......interaction  import InputEvent, InputManager
from ......display      import Surface
from ....element        import Element
from ....atoms          import Box
from ..interactable     import Interactable

from .dropdownselectcore         import DropdownselectCore
from .dropdownselectdata         import DropdownselectData

class Dropdownselect(Interactable[DropdownselectCore, DropdownselectData]):

    # -------------------- creation --------------------

    def __init__(self, core: DropdownselectCore, renderData: DropdownselectData, active: bool = True) -> None:
        super().__init__(core, renderData, active)
        self._renderData.alignInner(self)

    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'Dropdownselect':
        inner: list[Element] = args['inner']
        style: str = args['fixstyle']

        strOptions: list[str] = Dropdownselect.parseList(args['content'])
        numOptions: int = len(strOptions)

        genericHead: str = str(StyledDefault.TEXTBOX)
        genericDropdown: str = str(StyledDefault.BUTTON_TXT)
        specificHeads: list[Element] = []
        specificDropdowns: list[Element] = []
        for arg, v in args.items():
            match arg.lower():
                case 'customheads' | 'custheads' | 'specificheads' | 'spheads':
                    numSpecificHeads: int = int(Dropdownselect.parseNum(v))
                    specificHeads = inner[:numSpecificHeads]
                    if numSpecificHeads < len(inner):
                        specificDropdowns = inner[numSpecificHeads:]
                case 'generichead' | 'ghead' | 'head':
                    genericHead = str(v).strip()
                case 'genericdropdown' | 'genericdrop' | 'gdrop' | 'dropdown' | 'drop':
                    genericDropdown = str(v).strip()
        if not len(specificHeads) and not len(specificDropdowns):
            specificHeads = inner
        numOptions += len(specificDropdowns)

        dpdOptions: dict[str, Any] = {}
        for arg, v in args.items():
            match arg.lower():
                case 'vertical' | 'vert':
                    dpdOptions['vert'] = v
                case 'horizontal' | 'hor':
                    dpdOptions['hor'] = v
                case 'offset' | 'spacing':
                    dpdOptions['offset'] = v
                case 'size' | 'sizes' | 'sizing' | 'sizings':
                    dpdOptions['size'] = v

        startHead: Optional[Element] = Dropdownselect.getStyledElement(genericHead, style)
        startHead.set({'content':'SELECT'}) if startHead is not None else None
        heads: list[Element] = [Box.parseFromArgs({}) if startHead is None else startHead]
        drops: list[Element] = []
        optidx: int = 0
        for opt in range(numOptions):
            if opt < len(specificHeads):
                heads.append(specificHeads[opt])
            else:
                ghead = Dropdownselect.getStyledElement(genericHead, style)
                if ghead is None:
                    ghead = Box.parseFromArgs({})
                ghead.set({'content':strOptions[optidx]}, 1)
                heads.append(ghead)
            if opt < len(specificDropdowns):
                drops.append(specificDropdowns[opt])
            else:
                gdrop = Dropdownselect.getStyledElement(genericDropdown, style)
                if gdrop is None:
                    gdrop = Box.parseFromArgs({})
                gdrop.set({'content':strOptions[optidx]}, 1)
                drops.append(gdrop)
                optidx += 1

        button = Dropdownselect(DropdownselectCore(drops, **dpdOptions), DropdownselectData(heads))

        hasTrigger: bool = False
        for tag, value in args.items():
            match tag:
                case 'trigger':
                    hasTrigger = True
                    for v in Dropdownselect.parseList(value):
                        if v.lower() == 'click':
                            button._core.addTriggerEvent(InputManager.getEvent(InputEvent.LEFTDOWN))
                        else:
                            button._core.addTriggerEvent(InputManager.getEvent(InputEvent.fromStr(value)))
                case 'globaltrigger' | 'gtrigger' | 'global':
                    hasTrigger = True
                    for v in Dropdownselect.parseList(value):
                        if v.lower() == 'click':
                            button._core.addGlobalTriggerEvent(InputManager.getEvent(InputEvent.LEFTDOWN))
                        else:
                            button._core.addGlobalTriggerEvent(InputManager.getEvent(InputEvent.fromStr(value)))
        if not hasTrigger:
            button._core.addTriggerEvent(InputManager.getEvent(InputEvent.LEFTDOWN))
        return button

    @override
    def getInnerSizing(self, elSize: tuple[int, int], args: dict[str, Any]={}) -> tuple[int, int]:
        maxX, maxY = 0, 0
        for el in self._renderData.heads:
            cX, cY = el.getInnerSizing(elSize, args)
            maxX = max(cX, maxX)
            maxY = max(cY, maxY)
        return maxX, maxY

    # -------------------- access-point --------------------

    @override
    def _set(self, args: dict[str, Any], sets: int = -1, maxDepth: int = -1, skips: bool = False) -> bool:
        s: bool = super()._set(args, sets, maxDepth, skips)
        for tag, value in args.items():
            match tag:
                case 'subscribeToToggleState':
                    s = True
                    if not skips:
                        if isinstance(value, tuple) and isinstance(value[0], int) and isinstance(value[1], str):
                            self._core.subscribeToToggleState(value[0], value[1])
                        else:
                            raise ValueError('subscribeToSelect expects 2-tuple with the toggle state (int) and a callbackID')
                case 'unsubscribeToToggleState':
                    s = True
                    if not skips:
                        if isinstance(value, tuple) and isinstance(value[0], int) and isinstance(value[1], str):
                            self._core.unsubscribeToToggleState(value[0], value[1])
                        else:
                            raise ValueError('unsubscribeToToggleState expects 2-tuple with the toggle state (int) and a callbackID')
                case 'quickSubscribeToToggleState':
                    s = True
                    if not skips:
                        if isinstance(value, tuple) and isinstance(value[0], int) and isinstance(value[1], Callable) and isinstance(value[2], list):
                            self._core.quickSubscribeToToggleState(value[0], value[1], *value[2])
                        else:
                            raise ValueError('quickSubscribeToToggleState expects a 3-tuple the toggle state (int), with a Callable and a list of arguments')
        return s

    @override
    def set(self, args: dict[str, Any], sets: int = -1, maxDepth: int = -1, skips: list[int] = [0]) -> int:
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
    def setZIndex(self, zindex: int) -> None:
        super().setZIndex(zindex)
        for el in self._renderData.heads:
            el.setZIndex(zindex)
        self._core.getDropdown().setZIndex(zindex)

    @override
    def render(self, surface: Surface) -> None:
        """
        render renders the UI-Element onto the given surface

        Args:
            surface (Surface): the surface the UIElement should be drawn on
        """
        assert self._drawer is not None

        if self.isActive():
            self._core.getDropdown().render(surface)
            self._renderData.heads[self._core.getCurrentToggleState()].render(surface)

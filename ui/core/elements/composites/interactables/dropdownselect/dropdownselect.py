from typing import Any, Callable, override

from ......utility      import Rect
from ......interaction  import InputEvent, InputManager
from ......display      import Surface
from ....element        import Element
from ....atoms          import Text
from ..interactable     import Interactable

from .dropdownselectcore         import DropdownselectCore
from .dropdownselectdata         import DropdownselectData

default_nohead: dict[str, Any] = {'col':'white', 'content':'', 'fontsize':'d'}
default_nodpd : dict[str, Any] = {'col':'white', 'content':'', 'fontsize':'d'}
default_generic_head: str = 'dpdshead'
default_generic_dpd : str = 'dpdsbutton'

class Dropdownselect(Interactable[DropdownselectCore, DropdownselectData]):

    # -------------------- creation --------------------

    def __init__(self, core: DropdownselectCore, active: bool = True) -> None:

        super().__init__(core, DropdownselectData(), active)

    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'Dropdownselect':
        inner: list[Element] = args['inner']

        strOptions: list[str] = Dropdownselect.parseList(args['content'])
        numOptions: int = len(strOptions)

        style: str = ''
        genericHead: str = default_generic_head
        genericDropdown: str = default_generic_dpd
        specificHeads: list[Element] = []
        specificDropdowns: list[Element] = []
        for arg, v in args.items():
            if arg in Dropdownselect.styleTags:
                style = str(v).strip()
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

        heads: list[Element] = []
        drops: list[Element] = []
        optidx: int = 0
        for opt in range(numOptions):
            if opt < len(specificHeads):
                heads.append(specificHeads[opt])
            else:
                ghead = Dropdownselect.getStyledElement(genericHead, style)
                if ghead is None:
                    ghead = Text.parseFromArgs(default_nohead)
                ghead.set({'content':strOptions[optidx]}, 1)
                heads.append(ghead)
            if opt < len(specificDropdowns):
                drops.append(specificDropdowns[opt])
            else:
                gdrop = Dropdownselect.getStyledElement(genericDropdown, style)
                if gdrop is None:
                    gdrop = Text.parseFromArgs(default_nodpd)
                gdrop.set({'content':strOptions[optidx]}, 1)
                drops.append(gdrop)
                optidx += 1

        button = Dropdownselect(DropdownselectCore(Rect(), heads, drops, **dpdOptions))

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
        super().set(args, sets, maxDepth)
        for tag, value in args.items():
            match tag:
                case 'subscribeToToggleState':
                    if isinstance(value, tuple) and isinstance(value[0], int) and isinstance(value[1], str):
                        self._core.subscribeToToggleState(value[0], value[1])
                    else:
                        raise ValueError('subscribeToSelect expects 2-tuple with the toggle state (int) and a callbackID')
                case 'unsubscribeToToggleState':
                    if isinstance(value, tuple) and isinstance(value[0], int) and isinstance(value[1], str):
                        self._core.unsubscribeToToggleState(value[0], value[1])
                    else:
                        raise ValueError('unsubscribeToToggleState expects 2-tuple with the toggle state (int) and a callbackID')
                case 'quickSubscribeToToggleState':
                    if isinstance(value, tuple) and isinstance(value[0], int) and isinstance(value[1], Callable) and isinstance(value[2], list):
                        self._core.quickSubscribeToToggleState(value[0], value[1], *value[2])
                    else:
                        raise ValueError('quickSubscribeToToggleState expects a 3-tuple the toggle state (int), with a Callable and a list of arguments')
    
    # -------------------- rendering --------------------

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
            self._core.getOuter().render(surface)

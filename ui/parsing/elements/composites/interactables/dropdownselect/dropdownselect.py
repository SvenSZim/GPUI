from typing import Any, Callable, override

from ......utility      import Rect
from ......interaction  import InputEvent, InputManager
from ......display      import Surface
from ....element        import Element
from ....atoms          import Text, Box, Line
from ...addons          import Framed
from ..interactable     import Interactable

from .dropdownselectcore         import DropdownselectCore
from .dropdownselectdata         import DropdownselectData

class Dropdownselect(Interactable[DropdownselectCore, DropdownselectData]):

    # -------------------- creation --------------------

    def __init__(self, rect: Rect, *inner: tuple[tuple[Element, float], Element], verticalDropdown: bool=True,
                 offset: int=0, startState: int=0, active: bool = True, args: dict[str, Any]={}) -> None:
        
        super().__init__(DropdownselectCore(rect, *inner, verticalDropdown=verticalDropdown, offset=offset, startState=startState, args=args), DropdownselectData(), active)
    
    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'Dropdownselect':
        inner: list[Element] = args['inner']

        strOptions: list[str] = Dropdownselect.parseList(args['content'])
        numOptions: int = len(strOptions)

        specificHeads: list[Element] = []
        specificDropdowns: list[Element] = []
        for arg, v in args.items():
            match arg.lower():
                case 'custom' | 'innerspecifiers' | 'innercustom':
                    specifiers: list[int] = [int(Dropdownselect.parseNum(x)) for x in Dropdownselect.parseList(v)]
                    if len(specifiers) < 2:
                        raise ValueError('innercustom expects 2 arguments: specific head, specific dropdown')
                    numSpecificHeads, numSpecificDropdowns = specifiers[:2]
                    if len(inner) < numSpecificHeads + numSpecificDropdowns:
                        print('Dropdownselect::parseFromArgs custom specifiers do not match child-count!')
                    numOptions = min(numSpecificHeads + numOptions, numSpecificDropdowns + numOptions)
                    specificHeads = inner[:numSpecificHeads]
                    if numSpecificHeads < len(inner):
                        specificDropdowns = inner[numSpecificHeads:numSpecificHeads+numSpecificDropdowns]

        verticalDropdown = True
        offset = 0
        sizings: list[float] = [1.0 for _ in range(numOptions)]
        for arg, v in args.items():
            match arg.lower():
                case 'vertical' | 'vert':
                    verticalDropdown = True
                case 'horizontal' | 'hor':
                    verticalDropdown = False
                case 'offset' | 'spacing':
                    offset = int(Dropdownselect.extractNum(v))
                case 'size' | 'sizes' | 'sizing' | 'sizings':
                    sizings = list(map(Dropdownselect.parseNum, Dropdownselect.adjustList(list(map(str, sizings)), Dropdownselect.parseList(v))))
        
        genericHead: dict[str, Any] = {'col':'white'}
        genericDropdown: dict[str, Any] = {'col':'white'}
        if len(specificHeads) + len(specificDropdowns) < len(inner):
            remaining: list[Element] = inner[len(specificHeads) + len(specificDropdowns):]
            framedTypes: list[bool] = [any([isinstance(x, tp) for tp in [Framed, Line, Box]]) for x in remaining]
            if any(framedTypes):
                fi: int = framedTypes.index(True)
                framed1: Element = remaining[fi]
                if isinstance(framed1, Framed):
                    genericHead = framed1.getArgs()
                else:
                    genericHead = {'inner':[framed1]}
                if fi+1 < len(framedTypes) and any(framedTypes[fi+1:]):
                    f2: int = framedTypes.index(True, fi+1)
                    framed2: Element = remaining[f2]
                    if isinstance(framed2, Framed):
                        genericDropdown = framed2.getArgs()
                    else:
                        genericDropdown = {'inner':[framed2]}

        heads: list[Element] = []
        drops: list[Element] = []
        optidx: int = 0
        for opt in range(numOptions):
            useopt: bool = False
            if opt < len(specificHeads):
                heads.append(specificHeads[opt])
            else:
                ghead = genericHead.copy()
                if 'inner' not in ghead:
                    ghead['content'] = strOptions[optidx]
                    heads.append(Text.parseFromArgs(ghead))
                else:
                    ghead['inner'] = [x.copy() for x in ghead['inner']] + [Text.parseFromArgs({'content':strOptions[optidx], 'col':'white'})]
                    heads.append(Framed.parseFromArgs(ghead))
                useopt = True
            if opt < len(specificDropdowns):
                drops.append(specificDropdowns[opt])
            else:
                gdrop = genericDropdown.copy()
                if 'inner' not in gdrop:
                    gdrop['content'] = strOptions[optidx]
                    drops.append(Text.parseFromArgs(gdrop))
                else:
                    gdrop['inner'] = [x.copy() for x in gdrop['inner']] + [Text.parseFromArgs({'content':strOptions[optidx], 'col':'white'})]
                    drops.append(Framed.parseFromArgs(gdrop))
                useopt = True
            if useopt:
                optidx += 1
        
        button = Dropdownselect(Rect(), *zip(zip(drops, sizings), heads), verticalDropdown=verticalDropdown, offset=offset, args=args)
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
    def set(self, args: dict[str, Any]) -> None:
        super().set(args)
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

from dataclasses import dataclass
from typing import Any, override

from ......utility      import AlignType
from ....element            import Element
from ....atoms              import Line, Box
from ..interactabledata     import InteractableData

@dataclass
class SliderData(InteractableData):
    """
    SliderData is the storage class for all render-information
    for the interactable 'Slider'.
    """
    fillData: Box
    lineData: Line

    def alignInner(self, against: Element, horizontalSlider: bool) -> None:
        self.fillData.align(against)
        if horizontalSlider:
            self.fillData.alignSize(against, alignX=False)
            self.lineData.align(against, AlignType.iMiL)
        else:
            self.fillData.alignSize(against, alignY=False)
            self.lineData.align(against, AlignType.iTiM)

    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'SliderData':
        inner: list[Element] = args['inner']
        types = [0 if isinstance(x, Line) else 1 if isinstance(x, Box) else 2 for x in inner]
        fill = Box.parseFromArgs({})
        if 1 in types:
            fill = inner[types.index(1)]
        assert isinstance(fill, Box)
        line = Line.parseFromArgs({})
        if 0 in types:
            line = inner[types.index(0)]
        assert isinstance(line, Line)
        return SliderData(fill, line)

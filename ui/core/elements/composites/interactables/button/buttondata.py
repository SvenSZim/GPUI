from dataclasses import dataclass
from typing import Any, override

from ....element        import Element
from ....atoms              import Line, Box
from ..interactabledata     import InteractableData

@dataclass
class ButtonData(InteractableData):
    """
    ButtonData is the storage class for all render-information
    for the interactable 'Button'.
    """
    fillData: Box
    crossData: tuple[Line, Line]

    def alignInner(self, against: Element):
        self.fillData.align(against)
        self.fillData.alignSize(against)
        self.crossData[0].align(against)
        self.crossData[0].alignSize(against)
        self.crossData[1].align(against)
        self.crossData[1].alignSize(against)

    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'ButtonData':
        inner: list[Element] = args['inner']
        types = [0 if isinstance(x, Line) else 1 if isinstance(x, Box) else 2 for x in inner]
        fill = Box.parseFromArgs({})
        if 1 in types:
            fill = inner[types.index(1)]
        assert isinstance(fill, Box)
        cross1 = Line.parseFromArgs({})
        cross2 = Line.parseFromArgs({})
        if 0 in types:
            cross1 = inner[types.index(0)]
            if types.count(0) > 1:
                cross2 = inner[types.index(0, types.index(0)+1)]
            else:
                assert isinstance(cross1, Line)
                cross2 = cross1.copy()
        assert isinstance(cross1, Line) and isinstance(cross2, Line)
        cross2.set({'flip':True})
        return ButtonData(fill, (cross1, cross2))

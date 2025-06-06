from dataclasses import dataclass
from typing import Any, override

from ....element            import Element
from ..interactabledata     import InteractableData

@dataclass
class ToggleData(InteractableData):
    """
    ToggleData is the storage class for all render-information
    for the interactable 'Toggle'.
    """
    stateElements: list[Element]

    def alignInner(self, against: Element):
        for el in self.stateElements:
            el.align(against)
            el.alignSize(against)

    def setinner(self, args: dict[str, Any], sets: int = -1, maxDepth: int = -1, skips: list[int]=[0]) -> int:
        s: int = 0
        cs: int
        for el in self.stateElements:
            if sets < 0 or s < sets:
                cs = el.set(args, sets-s, maxDepth, skips)
                skips[0] = max(0, skips[0]-cs)
                s += cs
        return s

    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'ToggleData':
        return ToggleData([])

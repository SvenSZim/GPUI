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

    def setinner(self, args: dict[str, Any], sets: int = -1, maxDepth: int = -1) -> int:
        s: int = 0
        for el in self.stateElements:
            if sets < 0 or s < sets:
                s += el.set(args, sets-s, maxDepth)
        return s

    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'ToggleData':
        return ToggleData([])

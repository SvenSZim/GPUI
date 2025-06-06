from dataclasses import dataclass
from typing import Any, override

from ....element        import Element
from ..interactabledata import InteractableData

@dataclass
class DropdownselectData(InteractableData):
    """
    DropdownselectData is the storage class for all render-information
    for the interactable 'Dropdownselect'.
    """
    heads: list[Element]

    def alignInner(self, against: Element) -> None:
        for el in self.heads:
            el.align(against)
            el.alignSize(against)

    def setinner(self, args: dict[str, Any], sets: int=-1, maxDepth: int=-1, skips: list[int]=[0]) -> int:
        s: int = 0
        cs: int
        for el in self.heads:
            if sets < 0 or s < sets:
                cs = el.set(args, sets-s, maxDepth, skips)
                skips[0] = max(0, skips[0]-cs)
                s += cs
        return s

    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'DropdownselectData':
        return DropdownselectData([])

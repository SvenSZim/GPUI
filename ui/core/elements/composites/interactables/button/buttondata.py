from dataclasses import dataclass
from typing import Any, Optional, override

from ....element        import Element
from ..interactabledata     import InteractableData

@dataclass
class ButtonData(InteractableData):
    """
    ButtonData is the storage class for all render-information
    for the interactable 'Button'.
    """
    off: Element
    on: Optional[Element]

    def alignInner(self, against: Element):
        self.off.align(against)
        self.off.alignSize(against)
        if self.on is not None:
            self.on.align(against)
            self.on.alignSize(against)
    
    def setinner(self, args: dict[str, Any], sets: int = -1, maxDepth: int = -1, skips: list[int]=[0]) -> int:
        s: int = 0
        cs: int
        if sets < 0 or s < sets:
            cs = self.off.set(args, sets-s, maxDepth, skips)
            skips[0] = max(0, skips[0]-cs)
            s += cs
        if self.on is not None and (sets < 0 or s < sets):
            cs = self.on.set(args, sets-s, maxDepth, skips)
            skips[0] = max(0, skips[0]-cs)
            s += cs
        return s


    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'ButtonData':
        return ButtonData(args['off'], args['on'])

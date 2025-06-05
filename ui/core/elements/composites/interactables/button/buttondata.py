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
    
    def setinner(self, args: dict[str, Any], sets: int = -1, maxDepth: int = -1) -> int:
        s: int = self.off.set(args, sets, maxDepth)
        if self.on is not None and (sets < 0 or s < sets):
            s += self.on.set(args, sets-s, maxDepth)
        return s


    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'ButtonData':
        return ButtonData(args['off'], args['on'])

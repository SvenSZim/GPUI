from dataclasses import dataclass
from typing import Any, override

from ..interactabledata import InteractableData

from .....elements import Element
from ...addons import Grouped

@dataclass
class MultiselectData(InteractableData):
    """
    MultiselectData is the storage class for all render-information
    for the interactable 'Multiselect'.
    """

    group: Grouped

    def alignInner(self, against: Element):
        self.group.align(against)
        self.group.alignSize(against)

    def setinner(self, args: dict[str, Any], sets: int = -1, maxDepth: int = -1, skips: list[int] = [0]) -> int:
        return self.group.set(args, sets, maxDepth, skips)

    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'MultiselectData':
        return MultiselectData(Grouped.parseFromArgs({}))

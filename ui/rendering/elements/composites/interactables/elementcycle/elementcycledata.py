from dataclasses import dataclass
from typing import Any, override

from ..interactabledata     import InteractableData

@dataclass
class ElementCycleData(InteractableData):
    """
    ElementCycleData is the storage class for all render-information
    for the interactable 'ElementCycle'.
    """

    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'ElementCycleData':
        return ElementCycleData()

from dataclasses import dataclass
from typing import Any, override

from ..interactabledata import InteractableData

@dataclass
class MultiselectData(InteractableData):
    """
    MultiselectData is the storage class for all render-information
    for the interactable 'Multiselect'.
    """

    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'MultiselectData':
        return MultiselectData()

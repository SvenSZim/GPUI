from dataclasses import dataclass
from typing import Any, override

from ..interactabledata import InteractableData

@dataclass
class DropdownselectData(InteractableData):
    """
    DropdownselectData is the storage class for all render-information
    for the interactable 'Dropdownselect'.
    """

    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'DropdownselectData':
        return DropdownselectData()

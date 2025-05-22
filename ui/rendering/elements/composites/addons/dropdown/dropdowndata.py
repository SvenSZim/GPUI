from dataclasses import dataclass
from typing import Any, override

from ..addondata            import AddonData

@dataclass
class DropdownData(AddonData):
    """
    DropdownData is the storage class for all render-information
    for the addon 'Dropdown'.
    """
    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'DropdownData':
        return DropdownData()

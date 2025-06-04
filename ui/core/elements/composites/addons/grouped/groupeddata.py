from dataclasses import dataclass
from typing import Any, override

from ..addondata     import AddonData

@dataclass
class GroupedData(AddonData):
    """
    GroupedData is the storage class for all render-information
    for the addon 'Grouped'.
    """
    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'GroupedData':
        return GroupedData()
from dataclasses import dataclass
from typing import Any, override

from ..addondata     import AddonData

@dataclass
class StackedData(AddonData):
    """
    StackedData is the storage class for all render-information
    for the addon 'Stacked'.
    """
    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'StackedData':
        return StackedData()

from dataclasses import dataclass
from typing import Any, override

from ...elementdata     import ElementData

@dataclass
class UIData(ElementData):
    """
    UIData is the storage class for all render-information
    for the addon 'UI'.
    """

    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'UIData':
        return UIData()

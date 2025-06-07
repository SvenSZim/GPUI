from dataclasses import dataclass
from typing import Any, override

from ...elementdata     import ElementData

@dataclass
class SectionData(ElementData):
    """
    SectionData is the storage class for all render-information
    for the addon 'Section'.
    """
    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'SectionData':
        return SectionData()

from dataclasses import dataclass
from typing import Any, override

from ......utility  import AlignType
from ....element    import Element
from ....atoms      import Line
from ..addondata    import AddonData

@dataclass
class SectionData(AddonData):
    """
    SectionData is the storage class for all render-information
    for the addon 'Section'.
    """
    borderData        : tuple[Line, Line]

    def alignInner(self, against: Element, offset: int = 0) -> None:
        self.borderData[0].align(against, AlignType.iTM, offset=(0, -offset//2))
        self.borderData[0].alignSize(against, alignY=False)
        self.borderData[1].align(against, AlignType.iBM, offset=(0, offset//2))
        self.borderData[1].alignSize(against, alignY=False)

    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'SectionData':
        return SectionData((Line.parseFromArgs({}), Line.parseFromArgs({})))

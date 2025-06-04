from dataclasses import dataclass
from typing import Any, override

from ...element    import Element
from ...elementdata     import ElementData
from ...atoms      import Line

@dataclass
class SectionData(ElementData):
    """
    SectionData is the storage class for all render-information
    for the addon 'Section'.
    """
    borderData        : tuple[Line, Line]

    def alignInner(self, against: Element, sizings: tuple[float, float]) -> None:
        self.borderData[0].alignpoint(against, otherPoint=(0, sizings[0]))
        self.borderData[0].alignSize(against, alignY=False)
        self.borderData[1].alignpoint(against, otherPoint=(0, 1-sizings[1]))
        self.borderData[1].alignSize(against, alignY=False)

    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'SectionData':
        return SectionData((Line.parseFromArgs({'col':'white'}), Line.parseFromArgs({'col':'white'})))

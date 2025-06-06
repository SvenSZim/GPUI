from dataclasses import dataclass
from typing import Any, override

from ......utility  import AlignType
from ....element    import Element
from ....atoms      import Box
from ..addondata    import AddonData

@dataclass
class FramedData(AddonData):
    """
    FramedData is the storage class for all render-information
    for the addon 'Framed'.
    """
    fillData    : Element
    borderData  : tuple[Element, Element, Element, Element]

    def alignInner(self, against: Element) -> None:
        self.fillData.align(against)
        self.fillData.alignSize(against)
        self.borderData[0].align(against)
        self.borderData[0].align(against, AlignType.iBL, keepSize=False)
        self.borderData[1].align(against, AlignType.iTiR)
        self.borderData[1].align(against, AlignType.iBR, keepSize=False)
        self.borderData[2].align(against)
        self.borderData[2].align(against, AlignType.TiR, keepSize=False)
        self.borderData[3].align(against, AlignType.iBiL)
        self.borderData[3].align(against, AlignType.BiR, keepSize=False)

    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'FramedData':
        return FramedData(Box.parseFromArgs({}), (Box.parseFromArgs({}), Box.parseFromArgs({}), Box.parseFromArgs({}), Box.parseFromArgs({})))

    # -------------------- access-point --------------------

    def setinner(self, args: dict[str, Any], sets: int=-1, maxDepth: int=-1, skips: list[int]=[0]) -> int:
        s: int = 0
        cs: int
        for el in self.borderData:
            if sets < 0 or s < sets:
                cs = el.set(args, sets-s, maxDepth, skips)
                skips[0] = max(0, skips[0]-cs)
                s += cs
        if sets < 0 or s < sets:
            cs = self.fillData.set(args, sets-s, maxDepth, skips)
            skips[0] = max(0, skips[0]-cs)
            s += cs
        return s

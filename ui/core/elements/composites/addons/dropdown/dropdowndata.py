from dataclasses import dataclass
from typing import Any, override

from ......utility import AlignType, Rect
from ....element import Element
from ..addondata import AddonData
from ..grouped   import Grouped

@dataclass
class DropdownData(AddonData):
    """
    DropdownData is the storage class for all render-information
    for the addon 'Dropdown'.
    """
    dropdown: Grouped
    offset: int
    innercount: int
    innersize: float
    verticalDropdown: bool

    def alignInner(self, against: Element) -> None:
        if not self.innercount:
            return

        if self.verticalDropdown:
            self.dropdown.alignSize(against, relativeAlign=(1.0, self.innersize), absoluteOffset=(0, self.offset * (self.innercount-1)))
            self.dropdown.align(against, AlignType.BiL)
        else:
            self.dropdown.alignSize(against, relativeAlign=(self.innersize, 1.0), absoluteOffset=(self.offset * (self.innercount-1), 0))
            self.dropdown.align(against, AlignType.iTR)

    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'DropdownData':
        inner: list[Element] = args['inner']
        verticalDropdown = True
        offset = 0
        sizings: list[float] = [1.0 for _ in inner[1:]]
        for arg, v in args.items():
            match arg:
                case 'vertical' | 'vert':
                    verticalDropdown = True
                case 'horizontal' | 'hor':
                    verticalDropdown = False
                case 'offset' | 'spacing':
                    offset = int(DropdownData.extractNum(v))
                case 'size' | 'sizes' | 'sizing' | 'sizings':
                    sizings = list(map(DropdownData.parseNum, DropdownData.adjustList(list(map(str, sizings)), DropdownData.parseList(v))))
        gpd: Grouped = Grouped(Rect(), *zip(inner[1:], sizings), alignVertical=verticalDropdown, offset=offset)
        gpd.setActive(False)
        return DropdownData(gpd, offset, len(sizings), sum(sizings), verticalDropdown)

    # -------------------- access-point --------------------

    def set(self, args: dict[str, Any]) -> bool:
        return False

    def setinner(self, args: dict[str, Any], sets: int=-1, maxDepth: int=-1) -> int:
        return self.dropdown.set(args, sets, maxDepth)

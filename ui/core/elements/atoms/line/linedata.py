from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional, override

from .....utility import Color
from ..atomdata   import AtomData

class AltMode(Enum):
    DEFAULT = 0x00
    CROSS   = 0x01

@dataclass
class LineData(AtomData):
    """
    LineData is the storage class for all render-information
    for the atom 'Line'.
    """

    colors      : dict[str, Optional[Color]]                            = field(default_factory=lambda: {'': None})
    sizes       : dict[str, int | float]                                = field(default_factory=lambda: {'': 1.0})
    thickness   : dict[str, int]                                        = field(default_factory=lambda: {'': 1})
    altmode     : dict[str, AltMode]                                    = field(default_factory=lambda: {'': AltMode.DEFAULT})
    inset       : tuple[float, float] | float | tuple[int, int] | int   = 0
    flip        : bool                                                  = False
    order       : list[str]                                             = field(default_factory=lambda: [''])

    @override
    def copy(self) -> 'LineData':
        return LineData(deepcopy(self.colors), deepcopy(self.sizes),
                        deepcopy(self.thickness), deepcopy(self.altmode),
                        deepcopy(self.inset), deepcopy(self.flip),
                        deepcopy(self.order))

    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'LineData':
        data: LineData = LineData()
        data.set(args, False)
        return data

    # -------------------- access-point --------------------

    @override
    def set(self, args: dict[str, Any], skips: bool) -> bool:
        s: bool = False
        for arg, v in args.items():
            if arg not in ['inset', 'flip', 'sectionorder', 'order']:
                if not isinstance(v, str):
                    continue
                values = v.split(';')
                labelValuePairs: list[list[str]] = [vv.split(':') for vv in values]
                for vv in labelValuePairs:
                    label: str
                    value: str
                    if len(vv) == 1:
                        label = ''
                        value = vv[0]
                    else:
                        label = LineData.parseLabel(vv[0])
                        value = vv[1]
                    match arg:
                        case 'colors' | 'color' | 'col':
                            s = True
                            if not skips:
                                self.colors[label] = LineData.parseColor(value)
                        case 'thickness' | 'width':
                            s = True
                            if not skips:
                                self.thickness[label] = int(LineData.extractNum(value))
                        case 'sizes' | 'size':
                            s = True
                            if not skips:
                                match value:
                                    case 's':
                                        self.sizes[label] = 10
                                    case 'l':
                                        self.sizes[label] = 20
                                    case _:
                                        self.sizes[label] = LineData.parseNum(value)
                        case 'altmode' | 'mode':
                            s = True
                            if not skips:
                                match value:
                                    case 'cross':
                                        self.altmode[label] = AltMode.CROSS
            else:
                match arg:
                    case 'inset':
                        s = True
                        if not skips:
                            self.inset = LineData.parsePartial(v)
                    case 'flip':
                        s = True
                        if not skips:
                            self.flip = True
                    case 'sectionorder' | 'order':
                        s = True
                        if not skips:
                            self.order = LineData.parseList(v)
        return s

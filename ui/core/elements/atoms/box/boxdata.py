from dataclasses import dataclass, field
from copy import deepcopy
from enum import Enum
from typing import Any, Optional, override

from .....utility import Color
from ..atomdata import AtomData


bool4 = tuple[bool, bool, bool, bool]

class AltMode(Enum):
    DEFAULT         = 0x00
    STRIPED_V       = 0x01
    STRIPED_H       = 0x02
    CHECKERBOARD    = 0x03

class Filters(Enum):
    DEFAULT         = 0x00
    LINEAR          = 0x01
    QUADRATIC       = 0x03

@dataclass
class BoxData(AtomData):
    """
    BoxData is the storage class for all render-information
    for the atom 'Box'.
    """
    colors      : dict[str, Optional[Color]]    = field(default_factory=lambda:{'': None})
    partialInset: dict[str, tuple[float, float] | float | tuple[int, int] | int] = field(default_factory=lambda:{'': 0})
    partitioning: tuple[int, int, list[str]]    = field(default_factory=lambda:(1, 1, ['']))
    altMode     : dict[str, AltMode]            = field(default_factory=lambda:{'': AltMode.DEFAULT})
    orders      : dict[str, list[str]]          = field(default_factory=lambda:{'': ['']})
    altLen      : dict[str, float | int]        = field(default_factory=lambda:{'': 10})
    filters     : dict[str, Filters | tuple[Filters, tuple[float, float, tuple[float, float]], bool]] = field(default_factory=lambda:{'': Filters.DEFAULT})

    @override
    def copy(self) -> 'BoxData':
        return BoxData(deepcopy(self.colors), deepcopy(self.partialInset),
                       deepcopy(self.partitioning), deepcopy(self.altMode),
                       deepcopy(self.orders), deepcopy(self.altLen),
                       deepcopy(self.filters))

    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'BoxData':
        data: BoxData = BoxData()
        data.set(args, False)
        return data

    # -------------------- access-point --------------------

    @override
    def set(self, args: dict[str, Any], skips: bool) -> bool:
        s: bool = False
        for arg, v in args.items():
            if arg not in ['boxpart', 'partitioning', 'part']:
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
                        label = BoxData.parseLabel(vv[0])
                        value = vv[1]
                    match arg:
                        case 'boxinset' | 'inset' | 'partial' | 'shrink':
                            s = True
                            if not skips:
                                self.partialInset[label] = BoxData.parsePartial(value)
                        case 'boxcolor' | 'colors' | 'color' | 'col':
                            s = True
                            if not skips:
                                self.colors[label] = BoxData.parseColor(value)
                        case 'boxorder' | 'sectionorders' | 'orders' | 'ord':
                            s = True
                            if not skips:
                                self.orders[label] = BoxData.parseList(value)
                        case 'boxmode' | 'fillmodes' | 'fillmode' | 'fills' | 'fill' | 'altmodes' | 'altmode' | 'modes' | 'mode':
                            s = True
                            if not skips:
                                match value:
                                    case 'checkerboard' | 'cb':
                                        self.altMode[label] = AltMode.CHECKERBOARD
                                    case 'striped_vert' | 'strv':
                                        self.altMode[label] = AltMode.STRIPED_V
                                    case 'striped_hor' | 'strh':
                                        self.altMode[label] = AltMode.STRIPED_H
                        case 'boxsize' | 'fillsizes' | 'fillsize' | 'innersizings' | 'innersizing' | 'sizes' | 'size':
                            s = True
                            if not skips:
                                match value:
                                    case 's':
                                        self.altLen[label] = 10
                                    case 'l':
                                        self.altLen[label] = 20
                                    case _:
                                        self.altLen[label] = BoxData.parseNum(value)
                        case 'boxfilter' | 'filters' | 'filter' | 'filt':
                            s = True
                            if not skips:
                                filtype, *options = [vvv.strip() for vvv in value.split('=')]
                                if len(options) == 0:
                                    continue
                                inv: bool = False
                                if filtype[0] == 'i':
                                    inv = True
                                    filtype = filtype[1:]
                                match filtype[0].lower():
                                    case 'l' | 't':
                                        #linear/triangle filter
                                        self.filters[label] = (Filters.LINEAR, BoxData.parseFilterArgs(options[0]), inv)
                                    case 'q' | 'c':
                                        #quadratic/circle filter
                                        self.filters[label] = (Filters.QUADRATIC, BoxData.parseFilterArgs(options[0]), inv)
                                    case _:
                                        pass
            else:
                match arg:
                    case 'boxpart' | 'partitioning' | 'part':
                        s = True
                        if not skips:
                            self.partitioning = BoxData.parsePartition(v)

        return s

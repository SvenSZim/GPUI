from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any, Callable, Optional, override

from .....utility import Color
from ..atomdata import AtomData

def adjustedFontSizeFunction(medium: int, mediumFontSize: int, differenceAroundMedium: int, minFontSize: int) -> Callable[[int], int]:
    medium -= 1
    a: float = (mediumFontSize - differenceAroundMedium * medium - minFontSize) / (medium * medium * medium)
    b: float = -3.0 * a * medium
    c: float = differenceAroundMedium + 3.0 * a * medium * medium
    return lambda x: int(round(a * (x-1) * (x-1) * (x-1) + b * (x-1) * (x-1) + c * (x-1) + minFontSize, 0))

fontSizeFunction: Callable[[int], int] = adjustedFontSizeFunction(6, 24, 2, 8)

@dataclass
class TextData(AtomData):
    """
    TextData is the storage class for all render-information
    for the atom 'Text'.
    """
    inset       : tuple[float, float] | float | tuple[int, int] | int = 0
    dynamicText : bool                  = False
    textColor   : Optional[Color]       = None
    sysFontName : str                   = 'Arial'
    fontSize    : Optional[int]         = 24
    fontAlign   : tuple[float, float]   = field(default_factory=lambda: (0.5, 0.5))

    @override
    def copy(self) -> 'TextData':
        return TextData(deepcopy(self.inset), deepcopy(self.dynamicText),
                        deepcopy(self.textColor), deepcopy(self.sysFontName),
                        deepcopy(self.fontSize), deepcopy(self.fontAlign))
    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'TextData':
        data: TextData = TextData()
        for arg, value in args.items():
            match arg:
                case 'inset':
                    data.inset = TextData.parsePartial(value)
                case 'color' | 'col':
                    data.textColor = TextData.parseColor(value)
                case 'fontsize' | 'size':
                    if 'd' in value:
                        data.dynamicText = True
                    else:
                        sizeconv: dict[str, int] = {x:i for i, x in enumerate(['xxs','xs','s','ms','sm','m','lm','ml','l','xl','xxl'])}
                        if value.lower() in sizeconv:
                            data.fontSize = fontSizeFunction(sizeconv[value.lower()])
                        else:
                            data.fontSize = int(TextData.extractNum(value))
                case 'fontname' | 'sysfont' | 'font':
                    data.sysFontName = value
                case 'align':
                    if ',' in value:
                        xx, yy = 0.5, 0.5
                        x, y = [v.strip() for v in value.split(',')][:2]
                        if '.' in x:
                            vk, nk = [TextData.extractNum(v) for v in x.split('.')][:2]
                            xx = int(vk) + int(nk)/10**len(nk)
                        else:
                            match x.lower()[0]:
                                case 'l':
                                    xx = 0.0
                                case 'r':
                                    xx = 1.0
                        if '.' in y:
                            vk, nk = [TextData.extractNum(v) for v in y.split('.')][:2]
                            yy = int(vk) + int(nk)/10**len(nk)
                        else:
                            match y.lower()[0]:
                                case 't':
                                    yy = 0.0
                                case 'b':
                                    yy = 1.0
                        data.fontAlign = (xx, yy)
                    else:
                        xx = 0.5
                        x = value.strip()
                        if '.' in x:
                            vk, nk = [TextData.extractNum(v) for v in x.split('.')][:2]
                            xx = int(vk) + int(nk)/10**len(nk)
                        else:
                            match x.lower()[0]:
                                case 'l':
                                    xx = 0.0
                                case 'r':
                                    xx = 1.0
                        data.fontAlign = (xx, xx)
        return data

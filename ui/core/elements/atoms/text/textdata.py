from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any, Callable, Optional, override

from .....utility import tColor, Color
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
    TextData

    Storage for rendering parameters used by the `Text` atom.

    Fields
    - `inset` : either a number (absolute pixels or fractional when float) or
      a two-tuple describing horizontal/vertical insets. Floats are treated
      as fractions of the corresponding box dimension.
    - `dynamicText` : if True, `fontSize` is computed automatically to fit
      the available box.
    - `textColor` : Optional color specification accepted by `tColor`.
      Consumers should handle `tColor` instances as well as RGB/RGBA tuples
      and named/hex strings.
    - `sysFontName` : system font family name to use for rendering
    - `fontSize` : optional explicit font size (ignored when `dynamicText` is True)
    - `fontAlign` : tuple of horizontal and vertical alignment (0..1)

    Responsibilities
    - Provide parsing (`parseFromArgs`) and `set()` for applying attribute
      updates originating from XML/args. `set()` performs defensive type
      checks and raises informative errors for invalid input.
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
        data.set(args, False)
        return data

    # -------------------- access-point --------------------

    @override
    def set(self, args: dict[str, Any], skips: bool) -> bool:
        s: bool = False
        for arg, value in args.items():
            match arg:
                case 'inset':
                    s = True
                    if not skips:
                        self.inset = TextData.parsePartial(value)
                case 'color' | 'col':
                    s = True
                    if not skips:
                        try:
                            # tColor validates strings, tuples and names
                            self.textColor = tColor(value)
                        except Exception as e:
                            raise ValueError(f'invalid text color: {value}') from e
                case 'fontsize' | 'size':
                    s = True
                    if not skips:
                        if isinstance(value, str) and 'd' in value:
                            self.dynamicText = True
                        else:
                            sizeconv: dict[str, int] = {x:i for i, x in enumerate(['xxs','xs','s','ms','sm','m','lm','ml','l','xl','xxl'])}
                            if isinstance(value, str) and value.lower() in sizeconv:
                                self.fontSize = fontSizeFunction(sizeconv[value.lower()])
                            else:
                                try:
                                    self.fontSize = int(TextData.extractNum(str(value)))
                                except Exception:
                                    raise ValueError(f'invalid fontsize: {value}')
                case 'fontname' | 'sysfont' | 'font':
                    s = True
                    if not skips:
                        if not isinstance(value, str):
                            raise TypeError('fontname must be a string')
                        self.sysFontName = value
                case 'align':
                    s = True
                    if not skips:
                        if not isinstance(value, str):
                            raise TypeError('align must be a string')
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
                            self.fontAlign = (xx, yy)
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
                            self.fontAlign = (xx, xx)
        return s

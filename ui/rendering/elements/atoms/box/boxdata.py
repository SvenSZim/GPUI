from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, override

from .....utility import Color
from ....style import RenderStyle, StyleManager
from ..atomdata import AtomData
from .boxcreateoption import BoxCO
from .boxprefab import BoxPrefab


bool4 = tuple[bool, bool, bool, bool]

class AltMode(Enum):
    DEFAULT         = 0x00
    STRIPED_V       = 0x01
    STRIPED_H       = 0x02
    STRIPED_D       = 0x03
    STRIPED_DR      = 0x04
    CHECKERBOARD    = 0x05

@dataclass
class BoxData(AtomData[BoxCO, BoxPrefab]):
    """
    BoxData is the storage class for all render-information
    for the atom 'Box'.
    """
    partitioning: tuple[int, int, list[str]]    = field(default_factory=lambda:(1, 1, ['']))
    mainColor   : dict[str, Optional[Color]]    = field(default_factory=lambda:{'': None})
    altMode     : dict[str, Optional[AltMode]]  = field(default_factory=lambda:{'': None})
    altColor    : dict[str, Optional[Color]]    = field(default_factory=lambda:{'': None})
    altLen      : dict[str, float | int]        = field(default_factory=lambda:{'': 10})
    partialInset: dict[str, tuple[float, float] | float | tuple[int, int] | int] = field(default_factory=lambda:{'': 1.0})

    @override
    def __add__(self, extraData: tuple[BoxCO, RenderStyle]) -> 'BoxData':
        return self
        createOption: BoxCO = extraData[0]
        style: RenderStyle = extraData[1]
        if 0x1031 <= createOption.value < 0x103a:
            self.partial = 0.1 * (createOption.value - 0x1030)
        elif 0x1050 <= createOption.value < 0x1065:
            self.altMode = AltMode(createOption.value - 0x1050)
            if self.mainColor is None and self.altColor is None:
                self.mainColor = StyleManager.getStyleColor(0, style)
            if self.altAbsLen is None:
                self.altAbsLen = 10.0
        else:
            match createOption:
                case BoxCO.FILL_NOFILL:
                    self.mainColor = None
                case BoxCO.FILL_SOLID:
                    self.altMode = None
                    if self.mainColor is None:
                        self.mainColor = StyleManager.getStyleColor(0, style)
                case BoxCO.FILL_ALT:
                        self.altMode = AltMode.DEFAULT
                        if self.mainColor is None and self.altColor is None:
                            self.mainColor = StyleManager.getStyleColor(0, style)
                        if self.altAbsLen is None:
                            self.altAbsLen = 10.0
                
                case BoxCO.COLOR0:
                    self.mainColor = None
                case BoxCO.COLOR1:
                    self.mainColor = StyleManager.getStyleColor(0, style)
                case BoxCO.COLOR2:
                    self.mainColor = StyleManager.getStyleColor(1, style)

                case BoxCO.PARTIAL_NOPARTIAL:
                    self.partial = 1.0

                case BoxCO.ALTLENGTH10:
                    self.altAbsLen = 10.0
                case BoxCO.ALTLENGTH20:
                    self.altAbsLen = 20.0

                case BoxCO.ALTCOLOR0:
                    self.altColor = None
                case BoxCO.ALTCOLOR1:
                    self.altColor = StyleManager.getStyleColor(0, style)
                case BoxCO.ALTCOLOR2:
                    self.altColor = StyleManager.getStyleColor(1, style)
        return self

    @override
    def __mul__(self, extraData: tuple[BoxPrefab, RenderStyle]) -> 'BoxData':
        return self
        return {
            BoxPrefab.INVISIBLE     : lambda _     : BoxData(),
            BoxPrefab.BASIC         : lambda style : BoxData(mainColor=StyleManager.getStyleColor(0, style)),
            BoxPrefab.ALTCOLOR      : lambda style : BoxData(mainColor=StyleManager.getStyleColor(1, style))
        }[extraData[0]](extraData[1])

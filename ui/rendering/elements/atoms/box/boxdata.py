from dataclasses import dataclass
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
    mainColor   : Optional[Color]   = None
    altMode     : Optional[AltMode] = None
    altColor    : Optional[Color]   = None
    altAbsLen   : Optional[float]   = None

    @override
    def __add__(self, extraData: tuple[BoxCO, RenderStyle]) -> 'BoxData':
        createOption: BoxCO = extraData[0]
        style: RenderStyle = extraData[1]
        if 0x1030 <= createOption.value < 0x1045:
            self.altMode = AltMode(createOption.value - 0x1030)
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
                
                case BoxCO.FILL_COLOR1:
                    self.mainColor = StyleManager.getStyleColor(0, style)
                case BoxCO.FILL_COLOR2:
                    self.mainColor = StyleManager.getStyleColor(1, style)

                case BoxCO.ALTLENGTH10:
                    self.altAbsLen = 10.0
                case BoxCO.ALTLENGTH20:
                    self.altAbsLen = 20.0
                case BoxCO.ALTCOLOR1:
                    self.altColor = StyleManager.getStyleColor(0, style)
                case BoxCO.ALTCOLOR2:
                    self.altColor = StyleManager.getStyleColor(1, style)
        return self

    @override
    def __mul__(self, extraData: tuple[BoxPrefab, RenderStyle]) -> 'BoxData':
        return {
            BoxPrefab.INVISIBLE     : lambda _     : BoxData(),
            BoxPrefab.BASIC         : lambda style : BoxData(mainColor=StyleManager.getStyleColor(0, style)),
            BoxPrefab.ALTCOLOR      : lambda style : BoxData(mainColor=StyleManager.getStyleColor(1, style))
        }[extraData[0]](extraData[1])

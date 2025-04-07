from dataclasses import dataclass
from enum import Enum
from typing import Callable, Optional, override

from .....utility import Color
from ....style import RenderStyle, StyleManager
from ..atomdata import AtomData
from .textcreateoption import TextCO
from .textprefab import TextPrefab

class AlignType(Enum):
    TOPLEFT         = 0x00
    TOPCENTER       = 0x01
    TOPRIGHT        = 0x02
    CENTERLEFT      = 0x10
    CENTERCENTER    = 0x11
    CENTERRIGHT     = 0x12
    BOTTOMLEFT      = 0x20
    BOTTOMCENTER    = 0x21
    BOTTOMRIGHT     = 0x22

def adjustedFontSizeFunction(medium: int, mediumFontSize: int, differenceAroundMedium: int, minFontSize: int) -> Callable[[int], int]:
    medium -= 1
    a: float = (mediumFontSize - differenceAroundMedium * medium - minFontSize) / (medium * medium * medium)
    b: float = -3.0 * a * medium
    c: float = differenceAroundMedium + 3.0 * a * medium * medium
    return lambda x: int(round(a * (x-1) * (x-1) * (x-1) + b * (x-1) * (x-1) + c * (x-1) + minFontSize, 0))

fontSizeFunction: Callable[[int], int] = adjustedFontSizeFunction(6, 24, 2, 8)

@dataclass
class TextData(AtomData[TextCO, TextPrefab]):
    """
    TextData is the storage class for all render-information
    for the atom 'Text'.
    """
    dynamicText : bool              = False
    textColor   : Optional[Color]   = None
    sysFontName : str               = 'Arial'
    fontSize    : Optional[int]     = 24
    fontAlign   : AlignType         = AlignType.CENTERCENTER

    @override
    def __add__(self, extraData: tuple[TextCO, RenderStyle]) -> 'TextData':
        createOption: TextCO = extraData[0]
        style: RenderStyle = extraData[1]

        if 0x2010 == createOption.value:
            self.dynamicText = True
            self.fontSize = None
        elif 0x2010 < createOption.value < 0x2020:
            self.dynamicText = False
            self.fontSize = fontSizeFunction(createOption.value & 0xf)
        else:
            match createOption:
                case TextCO.NOTEXT:
                    self.textColor = None
                case TextCO.SOLID:
                    if self.textColor is None:
                        self.textColor = StyleManager.getStyleColor(0, style)

                case TextCO.COLOR1:
                    self.textColor = StyleManager.getStyleColor(0, style)
                case TextCO.COLOR2:
                    self.textColor = StyleManager.getStyleColor(1, style)

                case TextCO.ALIGNCENTER:
                    self.fontAlign = AlignType.CENTERCENTER
                case TextCO.ALIGNLEFT:
                    self.fontAlign = AlignType((self.fontAlign.value & 0xf0) + 0)
                case TextCO.ALIGNRIGHT:
                    self.fontAlign = AlignType((self.fontAlign.value & 0xf0) + 2)
                case TextCO.ALIGNTOP:
                    self.fontAlign = AlignType((self.fontAlign.value & 0xf) + 0)
                case TextCO.ALIGNBOTTOM:
                    self.fontAlign = AlignType((self.fontAlign.value & 0xf) + 2)
        return self

    @override
    def __mul__(self, extraData: tuple[TextPrefab, RenderStyle]) -> 'TextData':
        return {
            TextPrefab.BASIC           : lambda style : TextData(textColor=StyleManager.getStyleColor(0, style)),
            TextPrefab.DYNAMIC_BASIC   : lambda style : TextData(dynamicText=True, textColor=StyleManager.getStyleColor(0, style)),
        }[extraData[0]](extraData[1])

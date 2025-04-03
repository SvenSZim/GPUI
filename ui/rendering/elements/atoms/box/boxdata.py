from dataclasses import dataclass
from typing import Optional, override

from .....utility import Color
from ....style import RenderStyle, StyleManager
from ..atomdata import AtomData
from .boxcreateoption import BoxCO
from .boxprefab import BoxPrefab


bool4 = tuple[bool, bool, bool, bool]

@dataclass
class BoxData(AtomData[BoxCO, BoxPrefab]):
    """
    BoxData is the storage class for all render-information
    for the atom 'Box'.
    """
    fillColor   : Optional[Color]   = None
    doAlt       : bool              = False
    altColor    : Optional[Color]   = None

    @override
    def __add__(self, extraData: tuple[BoxCO, RenderStyle]) -> 'BoxData':
        createOption: BoxCO = extraData[0]
        style: RenderStyle = extraData[1]
        match createOption:
            case BoxCO.FILL_NOFILL:
                self.fillColor = None
            case BoxCO.FILL_SOLID:
                self.doAlt = False
                if self.fillColor is None:
                    self.fillColor = StyleManager.getStyleColor(0, style)
            
            case BoxCO.FILL_TOPLEFT:
                pass
            case BoxCO.FILL_TOPRIGHT:
                pass
            case BoxCO.FILL_BOTTOMLEFT:
                pass
            case BoxCO.FILL_BOTTOMRIGHT:
                pass

            case BoxCO.FILL_COLOR1:
                self.fillColor = StyleManager.getStyleColor(0, style)
            case BoxCO.FILL_COLOR2:
                self.fillColor = StyleManager.getStyleColor(1, style)
        return self

    @override
    def __mul__(self, extraData: tuple[BoxPrefab, RenderStyle]) -> 'BoxData':
        return {
            BoxPrefab.INVISIBLE     : lambda _     : BoxData(),
            BoxPrefab.BASIC         : lambda style : BoxData(fillColor=StyleManager.getStyleColor(0, style)),
            BoxPrefab.ALTCOLOR      : lambda style : BoxData(fillColor=StyleManager.getStyleColor(1, style))
        }[extraData[0]](extraData[1])

from dataclasses import dataclass
from typing import Optional, override

from .....utility import Color
from ....style    import RenderStyle, StyleManager
from ..atomdata   import AtomData
from .linecreateoption import LineCO
from .lineprefab  import LinePrefab


@dataclass
class LineData(AtomData[LineCO, LinePrefab]):
    """
    LineData is the storage class for all render-information
    for the atom 'Line'.
    """

    mainColor   : Optional[Color]   = None
    partial     : float             = 1.0
    doAlt       : bool              = False
    altAbsLen   : Optional[float]   = None
    altColor    : Optional[Color]   = None
    flip        : bool              = False

    @override
    def __add__(self, extraData: tuple[LineCO, RenderStyle]) -> 'LineData':
        style: RenderStyle = extraData[1]
        createOption: LineCO = extraData[0]
        if 0x021 <= createOption.value <= 0x030:
            self.partial = 0.1 * (createOption.value - 0x020)
        else:
            match createOption:
                case LineCO.TRANSPARENT:
                    self.mainColor = None
                    self.altColor = None
                case LineCO.SOLID:
                    self.doAlt = False
                    if self.mainColor is None:
                        self.mainColor = StyleManager.getStyleColor(0, style)
                case LineCO.DOTTED:
                    self.doAlt = True
                    if self.mainColor is not None and self.altColor is not None:
                        self.altColor = None
                    if self.altAbsLen is None:
                        self.altAbsLen = 10.0
                case LineCO.ALTERNATING:
                    self.doAlt = True
                    if self.mainColor is None:
                        self.mainColor = StyleManager.getStyleColor(0, style)
                    if self.altColor is None:
                        self.mainColor = StyleManager.getStyleColor(1, style)
                    if self.altAbsLen is None:
                        self.altAbsLen = 10.0

                case LineCO.NOFLIP:
                    self.flip = False
                case LineCO.FLIPPED:
                    self.flip = True
                
                case LineCO.COLOR0:
                    self.mainColor = None
                case LineCO.COLOR1:
                    self.mainColor = StyleManager.getStyleColor(0, style)
                case LineCO.COLOR2:
                    self.mainColor = StyleManager.getStyleColor(1, style)

                case LineCO.PARTIAL_NOPARTIAL:
                    self.partial = 1.0

                case LineCO.ALTLENGTH10:
                    self.altAbsLen = 10.0
                case LineCO.ALTLENGTH20:
                    self.altAbsLen = 20.0

                case LineCO.ALTCOLOR0:
                    self.altColor = None
                case LineCO.ALTCOLOR1:
                    self.altColor = StyleManager.getStyleColor(0, style)
                case LineCO.ALTCOLOR2:
                    self.altColor = StyleManager.getStyleColor(1, style)
        return self


    @override
    def __mul__(self, extraData: tuple[LinePrefab, RenderStyle]) -> 'LineData':
        return {
            LinePrefab.INVISIBLE   : lambda _     : LineData(),
            LinePrefab.SOLID       : lambda style : LineData(StyleManager.getStyleColor(0, style)),
            LinePrefab.DOTTED      : lambda style : LineData(StyleManager.getStyleColor(0, style), doAlt=True, altAbsLen=10.0),
            LinePrefab.ALTERNATING : lambda style : LineData(StyleManager.getStyleColor(0, style), doAlt=True, altAbsLen=10.0, altColor=StyleManager.getStyleColor(1, style)),
            LinePrefab.SHRINKED    : lambda style : LineData(StyleManager.getStyleColor(0, style), partial=0.75),
            LinePrefab.SHRINKED_DOTTED:lambda style : LineData(StyleManager.getStyleColor(0, style), partial=0.75, doAlt=True, altAbsLen=10.0),
        }[extraData[0]](extraData[1])

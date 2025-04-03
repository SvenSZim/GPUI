from dataclasses import dataclass
from typing import Optional, override

from .....utility import Color
from ....style import RenderStyle, StyleManager
from ..atomdata import AtomData
from .textcreateoption import TextCO
from .textprefab import TextPrefab


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

    @override
    def __add__(self, extraData: tuple[TextCO, RenderStyle]) -> 'TextData':
        createOption: TextCO = extraData[0]
        style: RenderStyle = extraData[1]
        match createOption:
            case TextCO.NOTEXT:
                self.textColor = None
            case TextCO.SOLID:
                if self.textColor is None:
                    self.textColor = StyleManager.getStyleColor(0, style)

            case TextCO.STATIC:
                self.dynamicText = False
                if self.fontSize is None:
                    self.fontSize = 24
            case TextCO.DYNAMIC:
                self.dynamicText = True
                self.fontSize = None

            case TextCO.COLOR1:
                self.textColor = StyleManager.getStyleColor(0, style)
            case TextCO.COLOR2:
                self.textColor = StyleManager.getStyleColor(1, style)
        return self

    @override
    def __mul__(self, extraData: tuple[TextPrefab, RenderStyle]) -> 'TextData':
        return {
            TextPrefab.BASIC           : lambda style : TextData(textColor=StyleManager.getStyleColor(0, style)),
            TextPrefab.DYNAMIC_BASIC   : lambda style : TextData(dynamicText=True, textColor=StyleManager.getStyleColor(0, style)),
        }[extraData[0]](extraData[1])

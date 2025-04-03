from dataclasses import dataclass, field
from typing import Optional, override

from .....createinfo import CreateInfo
from .....style      import RenderStyle
from ....atoms       import AtomCreateOption, Line, LineData, LineCO, Box, BoxData, BoxCO
from ..addondata     import AddonData
from .framedcreateoption import FramedCO
from .framedprefab   import FramedPrefab

@dataclass
class FramedData(AddonData[FramedCO, FramedPrefab]):
    """
    FramedData is the storage class for all render-information
    for the addon 'Framed'.
    """
    fillData : Optional[CreateInfo[Box]] = None
    borderData: Optional[tuple[CreateInfo[Line], CreateInfo[Line], CreateInfo[Line], CreateInfo[Line]]] = None

    createActiveBorder: list[bool] = field(default_factory=lambda:[True, True, True, True])
    createFillData: BoxData = field(default_factory=BoxData)
    createBorderData: tuple[LineData, LineData, LineData, LineData] = field(default_factory=lambda:(LineData(), LineData(), LineData(), LineData()))

    @override
    def __add__(self, extraData: tuple[FramedCO | AtomCreateOption, RenderStyle]) -> 'FramedData':
        createOption: FramedCO | AtomCreateOption = extraData[0]
        style: RenderStyle = extraData[1]
        if createOption.value < 0x1000:
            for active, data in zip(self.createActiveBorder, self.createBorderData):
                if active:
                    data += (LineCO(createOption.value), style)
        elif createOption.value < 0x2000:
            self.createFillData += (BoxCO(createOption.value), style)
        elif createOption.value == 0x8000:
            self.fillData = CreateInfo(Box, renderData=self.createFillData)
            self.borderData = (CreateInfo(Line, renderData=self.createBorderData[0]),
                               CreateInfo(Line, renderData=self.createBorderData[1]),
                               CreateInfo(Line, renderData=self.createBorderData[2]),
                               CreateInfo(Line, renderData=self.createBorderData[3]))
        elif 0x8000 < createOption.value < 0x8800:
            self.createActiveBorder[0] = bool(createOption.value & 1)
            self.createActiveBorder[1] = bool(createOption.value & 2)
            self.createActiveBorder[2] = bool(createOption.value & 4)
            self.createActiveBorder[3] = bool(createOption.value & 8)

        return self

    @override
    def __mul__(self, extraData: tuple[FramedPrefab, RenderStyle]) -> 'FramedData':
        return self

from dataclasses import dataclass, field
from typing import override

from .....createinfo import CreateInfo
from .....style      import RenderStyle
from ....atoms       import AtomCreateOption, Line, LineCO, LinePrefab, Box, BoxCO, BoxPrefab
from ..addondata     import AddonData
from .framedcreateoption import FramedCO
from .framedprefab   import FramedPrefab

@dataclass
class FramedData(AddonData[FramedCO, FramedPrefab]):
    """
    FramedData is the storage class for all render-information
    for the addon 'Framed'.
    """
    fillData          : CreateInfo[Box]                                                               = field(default_factory=lambda: CreateInfo(Box, BoxPrefab.INVISIBLE))
    borderData        : tuple[CreateInfo[Line], CreateInfo[Line], CreateInfo[Line], CreateInfo[Line]] = field(default_factory=lambda:(CreateInfo(Line, LinePrefab.INVISIBLE),
                                                                                                                                      CreateInfo(Line, LinePrefab.INVISIBLE),
                                                                                                                                      CreateInfo(Line, LinePrefab.INVISIBLE),
                                                                                                                                      CreateInfo(Line, LinePrefab.INVISIBLE)))
    createActiveBorder: list[bool]                                                    = field(default_factory=lambda:[True, True, True, True])
    createFillData    : list[BoxCO]                                                   = field(default_factory=lambda:[])
    createBorderData  : tuple[list[LineCO], list[LineCO], list[LineCO], list[LineCO]] = field(default_factory=lambda:([], [], [], []))

    @override
    def __add__(self, extraData: tuple[FramedCO | AtomCreateOption, RenderStyle]) -> 'FramedData':
        createOption: FramedCO | AtomCreateOption = extraData[0]
        if createOption.value < 0x1000:
            for active, data in zip(self.createActiveBorder, self.createBorderData):
                if active:
                    data.append(LineCO(createOption.value))
        elif createOption.value < 0x2000:
            self.createFillData.append(BoxCO(createOption.value))
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

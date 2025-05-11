from dataclasses import dataclass, field
from typing import override

from .....style      import RenderStyle
from ....atoms       import AtomCreateOption, LineCO, BoxCO
from ..addondata     import AddonData
from .framedcreateoption import FramedCO
from .framedprefab   import FramedPrefab

@dataclass
class FramedData(AddonData[FramedCO, FramedPrefab]):
    """
    FramedData is the storage class for all render-information
    for the addon 'Framed'.
    """
    fillData    : list[BoxCO]                                                   = field(default_factory=lambda:[])
    borderData  : tuple[list[LineCO], list[LineCO], list[LineCO], list[LineCO]] = field(default_factory=lambda:([], [], [], []))

    createActiveBorder: list[bool]                                                    = field(default_factory=lambda:[True, True, True, True])

    @override
    def __add__(self, extraData: tuple[FramedCO | AtomCreateOption, RenderStyle]) -> 'FramedData':
        return self
        createOption: FramedCO | AtomCreateOption = extraData[0]
        if createOption.value < 0x1000:
            for active, data in zip(self.createActiveBorder, self.borderData):
                if active:
                    data.append(LineCO(createOption.value))
        elif createOption.value < 0x2000:
            self.fillData.append(BoxCO(createOption.value))
        elif 0x8000 < createOption.value < 0x8800:
            self.createActiveBorder[0] = bool(createOption.value & 1)
            self.createActiveBorder[1] = bool(createOption.value & 2)
            self.createActiveBorder[2] = bool(createOption.value & 4)
            self.createActiveBorder[3] = bool(createOption.value & 8)

        return self

    @override
    def __mul__(self, extraData: tuple[FramedPrefab, RenderStyle]) -> 'FramedData':
        return self
        return {
            FramedPrefab.BASIC       : lambda _     : FramedData(),
            FramedPrefab.BORDERED    : lambda style : FramedData() + (LineCO.COLOR1, extraData[1]),
        }[extraData[0]](extraData[1])

from dataclasses import dataclass, field
from typing import override

from .....style      import RenderStyle
from ....atoms       import AtomCreateOption, LineCO
from ..addondata     import AddonData
from .sectioncreateoption import SectionCO
from .sectionprefab  import SectionPrefab

@dataclass
class SectionData(AddonData[SectionCO, SectionPrefab]):
    """
    SectionData is the storage class for all render-information
    for the addon 'Section'.
    """
    createActiveBorder: list[bool]                                                    = field(default_factory=lambda:[True, True])
    borderData        : tuple[list[LineCO], list[LineCO], list[LineCO], list[LineCO]] = field(default_factory=lambda:([], [], [], []))

    @override
    def __add__(self, extraData: tuple[SectionCO | AtomCreateOption, RenderStyle]) -> 'SectionData':
        createOption: SectionCO | AtomCreateOption = extraData[0]
        if createOption.value < 0x1000:
            for active, data in zip(self.createActiveBorder, self.borderData):
                if active:
                    data.append(LineCO(createOption.value))
        elif 0xa000 < createOption.value < 0xa004:
            self.createActiveBorder[0] = bool(createOption.value & 1)
            self.createActiveBorder[1] = bool(createOption.value & 2)
        return self

    @override
    def __mul__(self, extraData: tuple[SectionPrefab, RenderStyle]) -> 'SectionData':
        return self

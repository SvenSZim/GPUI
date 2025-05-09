from dataclasses import dataclass, field
from typing import override

from .....style             import RenderStyle
from ....atoms              import AtomCreateOption, LineCO, BoxCO
from ..interactabledata     import InteractableData
from .checkboxcreateoption  import CheckboxCO
from .checkboxprefab        import CheckboxPrefab

@dataclass
class CheckboxData(InteractableData[CheckboxCO, CheckboxPrefab]):
    """
    CheckboxData is the storage class for all render-information
    for the interactable 'Checkbox'.
    """
    createActive: list[bool]                           = field(default_factory=lambda:[True, False, False])
    fillData: list[BoxCO]                        = field(default_factory=lambda:[])
    crossData: tuple[list[LineCO], list[LineCO]] = field(default_factory=lambda:([], []))

    @override
    def __add__(self, extraData: tuple[CheckboxCO | AtomCreateOption, RenderStyle]) -> 'CheckboxData':
        createOption: CheckboxCO | AtomCreateOption = extraData[0]
        if createOption.value < 0x1000:
            if self.createActive[1]:
                self.crossData[0].append(LineCO(createOption.value))
            if self.createActive[2]:
                self.crossData[1].append(LineCO(createOption.value))
        elif createOption.value < 0x2000:
            if self.createActive[0]:
                self.fillData.append(BoxCO(createOption.value))
        elif createOption.value == 0x10200:
            self.crossData[1].append(LineCO.FLIPPED)
            if self.createActive[0]:
                self.crossData = ([], [])
            else:
                self.fillData = []
        else:
            match createOption:
                case CheckboxCO.USEBOX:
                    self.createActive[0] = True
                    self.createActive[1] = False
                    self.createActive[2] = False
                case CheckboxCO.USECROSS:
                    self.createActive[0] = False
                    self.createActive[1] = True
                    self.createActive[2] = True
                case CheckboxCO.USECROSS_TL:
                    self.createActive[0] = False
                    self.createActive[1] = True
                    self.createActive[2] = False
                case CheckboxCO.USECROSS_TR:
                    self.createActive[0] = False
                    self.createActive[1] = False
                    self.createActive[2] = True

        return self

    @override
    def __mul__(self, extraData: tuple[CheckboxPrefab, RenderStyle]) -> 'CheckboxData':
        return self

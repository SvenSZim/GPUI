from dataclasses import dataclass, field
from typing import override

from .....style             import RenderStyle
from ....atoms              import AtomCreateOption, LineCO, BoxCO
from ..interactabledata     import InteractableData
from .buttoncreateoption  import ButtonCO
from .buttonprefab        import ButtonPrefab

@dataclass
class ButtonData(InteractableData[ButtonCO, ButtonPrefab]):
    """
    ButtonData is the storage class for all render-information
    for the interactable 'Button'.
    """
    createActive: list[bool]                           = field(default_factory=lambda:[True, False, False])
    fillData: list[BoxCO]                        = field(default_factory=lambda:[])
    crossData: tuple[list[LineCO], list[LineCO]] = field(default_factory=lambda:([], []))

    @override
    def __add__(self, extraData: tuple[ButtonCO | AtomCreateOption, RenderStyle]) -> 'ButtonData':
        createOption: ButtonCO | AtomCreateOption = extraData[0]
        if createOption.value < 0x1000:
            if self.createActive[1]:
                self.crossData[0].append(LineCO(createOption.value))
            if self.createActive[2]:
                self.crossData[1].append(LineCO(createOption.value))
        elif createOption.value < 0x2000:
            if self.createActive[0]:
                self.fillData.append(BoxCO(createOption.value))
        elif createOption.value == 0x10100:
            self.crossData[1].append(LineCO.FLIPPED)
            if self.createActive[0]:
                self.crossData = ([], [])
            else:
                self.fillData = []
        else:
            match createOption:
                case ButtonCO.USEBOX:
                    self.createActive[0] = True
                    self.createActive[1] = False
                    self.createActive[2] = False
                case ButtonCO.USECROSS:
                    self.createActive[0] = False
                    self.createActive[1] = True
                    self.createActive[2] = True
                case ButtonCO.USECROSS_TL:
                    self.createActive[0] = False
                    self.createActive[1] = True
                    self.createActive[2] = False
                case ButtonCO.USECROSS_TR:
                    self.createActive[0] = False
                    self.createActive[1] = False
                    self.createActive[2] = True

        return self

    @override
    def __mul__(self, extraData: tuple[ButtonPrefab, RenderStyle]) -> 'ButtonData':
        return self

from dataclasses import dataclass, field
from typing import override

from .....createinfo        import CreateInfo
from .....style             import RenderStyle
from ....atoms              import AtomCreateOption, Line, LineCO, LinePrefab, Box, BoxCO, BoxPrefab
from ..interactabledata     import InteractableData
from .buttoncreateoption  import ButtonCO
from .buttonprefab        import ButtonPrefab

@dataclass
class ButtonData(InteractableData[ButtonCO, ButtonPrefab]):
    """
    ButtonData is the storage class for all render-information
    for the interactable 'Button'.
    """
    fillData : CreateInfo[Box]                           = field(default_factory=lambda: CreateInfo(Box, renderData=BoxPrefab.INVISIBLE))
    crossData: tuple[CreateInfo[Line], CreateInfo[Line]] = field(default_factory=lambda:(CreateInfo(Line, renderData=LinePrefab.INVISIBLE),
                                                                                         CreateInfo(Line, renderData=LinePrefab.INVISIBLE)))

    createActive: list[bool]                           = field(default_factory=lambda:[True, False, False])
    createFillData: list[BoxCO]                        = field(default_factory=lambda:[])
    createCrossData: tuple[list[LineCO], list[LineCO]] = field(default_factory=lambda:([], []))

    @override
    def __add__(self, extraData: tuple[ButtonCO | AtomCreateOption, RenderStyle]) -> 'ButtonData':
        createOption: ButtonCO | AtomCreateOption = extraData[0]
        if createOption.value < 0x1000:
            if self.createActive[1]:
                self.createCrossData[0].append(LineCO(createOption.value))
            if self.createActive[2]:
                self.createCrossData[1].append(LineCO(createOption.value))
        elif createOption.value < 0x2000:
            if self.createActive[0]:
                self.createFillData.append(BoxCO(createOption.value))
        elif createOption.value == 0x10100:
            self.createCrossData[1].append(LineCO.FLIPPED)
            self.fillData = CreateInfo(Box, renderData=BoxPrefab.INVISIBLE)
            self.crossData = (CreateInfo(Line, renderData=LinePrefab.INVISIBLE),
                               CreateInfo(Line, renderData=LinePrefab.INVISIBLE))
            if self.createActive[0]:
                self.fillData = CreateInfo(Box, renderData=self.createFillData)
            else:
                self.crossData = (CreateInfo(Line, renderData=self.createCrossData[0]),
                                   CreateInfo(Line, renderData=self.createCrossData[1]))
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

from dataclasses import dataclass, field
from typing import override

from .....createinfo        import CreateInfo
from .....style             import RenderStyle
from ....atoms              import AtomCreateOption, Line, LineCO, LinePrefab, Box, BoxCO, BoxPrefab
from ..interactabledata     import InteractableData
from .slidercreateoption    import SliderCO
from .sliderprefab          import SliderPrefab

@dataclass
class SliderData(InteractableData[SliderCO, SliderPrefab]):
    """
    SliderData is the storage class for all render-information
    for the interactable 'Slider'.
    """
    fillData : CreateInfo[Box]  = field(default_factory=lambda: CreateInfo(Box, renderData=BoxPrefab.INVISIBLE))
    lineData : CreateInfo[Line] = field(default_factory=lambda:CreateInfo(Line, renderData=LinePrefab.INVISIBLE))

    doCreateBoxFill: bool           = True
    createFillData: list[BoxCO]     = field(default_factory=lambda:[])
    createLineData: list[LineCO]    = field(default_factory=lambda:[])

    @override
    def __add__(self, extraData: tuple[SliderCO | AtomCreateOption, RenderStyle]) -> 'SliderData':
        createOption: SliderCO | AtomCreateOption = extraData[0]
        if createOption.value < 0x1000:
            self.createLineData.append(LineCO(createOption.value))
        elif createOption.value < 0x2000:
            self.createFillData.append(BoxCO(createOption.value))
        elif createOption.value == 0x10400:
            self.fillData = CreateInfo(Box, renderData=BoxPrefab.INVISIBLE)
            self.crossData = CreateInfo(Line, renderData=LinePrefab.INVISIBLE)
            if self.doCreateBoxFill:
                self.fillData = CreateInfo(Box, renderData=self.createFillData)
            else:
                self.lineData = CreateInfo(Line, renderData=self.createLineData)
        else:
            match createOption:
                case SliderCO.USEBOX:
                    self.doCreateBoxFill = True
                case SliderCO.USELINE:
                    self.doCreateBoxFill = False

        return self

    @override
    def __mul__(self, extraData: tuple[SliderPrefab, RenderStyle]) -> 'SliderData':
        return self

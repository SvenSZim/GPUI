from dataclasses import dataclass, field
from typing import override

from .....style             import RenderStyle
from ....atoms              import AtomCreateOption, LineCO, BoxCO
from ..interactabledata     import InteractableData
from .slidercreateoption    import SliderCO
from .sliderprefab          import SliderPrefab

@dataclass
class SliderData(InteractableData[SliderCO, SliderPrefab]):
    """
    SliderData is the storage class for all render-information
    for the interactable 'Slider'.
    """
    doCreateBoxFill: bool     = True
    fillData: list[BoxCO]     = field(default_factory=lambda:[])
    lineData: list[LineCO]    = field(default_factory=lambda:[])

    @override
    def __add__(self, extraData: tuple[SliderCO | AtomCreateOption, RenderStyle]) -> 'SliderData':
        createOption: SliderCO | AtomCreateOption = extraData[0]
        if createOption.value < 0x1000:
            self.lineData.append(LineCO(createOption.value))
        elif createOption.value < 0x2000:
            self.fillData.append(BoxCO(createOption.value))
        elif createOption.value == 0x10400:
            if self.doCreateBoxFill:
                self.lineData = []
            else:
                self.fillData = []
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

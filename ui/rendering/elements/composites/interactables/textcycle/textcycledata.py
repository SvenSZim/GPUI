from dataclasses import dataclass, field
from typing import override

from .....createinfo        import CreateInfo
from .....style             import RenderStyle
from ....atoms              import AtomCreateOption, Text, TextCO, TextPrefab
from ..interactabledata     import InteractableData
from .textcyclecreateoption import TextCycleCO
from .textcycleprefab       import TextCyclePrefab

@dataclass
class TextCycleData(InteractableData[TextCycleCO, TextCyclePrefab]):
    """
    TextCycleData is the storage class for all render-information
    for the interactable 'TextCycle'.
    """
    textData      : CreateInfo[Text]    = field(default_factory=lambda: CreateInfo(Text, renderData=TextPrefab.BASIC))
    createTextData: list[TextCO]        = field(default_factory=lambda:[])

    @override
    def __add__(self, extraData: tuple[TextCycleCO | AtomCreateOption, RenderStyle]) -> 'TextCycleData':
        createOption: TextCycleCO | AtomCreateOption = extraData[0]
        if 0x2000 <= createOption.value < 0x3000:
            self.createTextData.append(TextCO(createOption.value))
        elif createOption.value == 0x10600:
            self.textData = CreateInfo(Text, renderData=self.createTextData)
        return self

    @override
    def __mul__(self, extraData: tuple[TextCyclePrefab, RenderStyle]) -> 'TextCycleData':
        return self

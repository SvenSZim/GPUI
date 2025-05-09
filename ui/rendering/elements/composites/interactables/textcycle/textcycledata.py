from dataclasses import dataclass, field
from typing import override

from .....style             import RenderStyle
from ....atoms              import AtomCreateOption, TextCO
from ..interactabledata     import InteractableData
from .textcyclecreateoption import TextCycleCO
from .textcycleprefab       import TextCyclePrefab

@dataclass
class TextCycleData(InteractableData[TextCycleCO, TextCyclePrefab]):
    """
    TextCycleData is the storage class for all render-information
    for the interactable 'TextCycle'.
    """
    textData: list[TextCO]        = field(default_factory=lambda:[])

    @override
    def __add__(self, extraData: tuple[TextCycleCO | AtomCreateOption, RenderStyle]) -> 'TextCycleData':
        createOption: TextCycleCO | AtomCreateOption = extraData[0]
        if 0x2000 <= createOption.value < 0x3000:
            self.textData.append(TextCO(createOption.value))
        return self

    @override
    def __mul__(self, extraData: tuple[TextCyclePrefab, RenderStyle]) -> 'TextCycleData':
        return self

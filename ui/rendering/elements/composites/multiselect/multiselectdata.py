from dataclasses import dataclass
from typing import override

from ....style             import RenderStyle
from ..compositiondata     import CompositionData
from .multiselectcreateoption import MultiselectCO
from .multiselectprefab       import MultiselectPrefab

@dataclass
class MultiselectData(CompositionData[MultiselectCO, MultiselectPrefab]):
    """
    MultiselectData is the storage class for all render-information
    for the interactable 'Multiselect'.
    """

    @override
    def __add__(self, extraData: tuple[MultiselectCO, RenderStyle]) -> 'MultiselectData':
        return self

    @override
    def __mul__(self, extraData: tuple[MultiselectPrefab, RenderStyle]) -> 'MultiselectData':
        return self

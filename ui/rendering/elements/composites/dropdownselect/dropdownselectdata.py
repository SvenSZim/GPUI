from dataclasses import dataclass
from typing import override

from ....style            import RenderStyle
from ..compositiondata    import CompositionData
from .dropdownselectcreateoption  import DropdownselectCO
from .dropdownselectprefab        import DropdownselectPrefab

@dataclass
class DropdownselectData(CompositionData[DropdownselectCO, DropdownselectPrefab]):
    """
    DropdownselectData is the storage class for all render-information
    for the interactable 'Dropdownselect'.
    """

    @override
    def __add__(self, extraData: tuple[DropdownselectCO, RenderStyle]) -> 'DropdownselectData':
        return self

    @override
    def __mul__(self, extraData: tuple[DropdownselectPrefab, RenderStyle]) -> 'DropdownselectData':
        return self

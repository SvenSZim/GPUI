from dataclasses import dataclass, field
from typing import override

from .....createinfo        import CreateInfo
from .....style             import RenderStyle
from ....atoms              import AtomCreateOption, Line, LineCO, LinePrefab, Box, BoxCO, BoxPrefab
from ..addondata            import AddonData
from .dropdowncreateoption  import DropdownCO
from .dropdownprefab        import DropdownPrefab

@dataclass
class DropdownData(AddonData[DropdownCO, DropdownPrefab]):
    """
    DropdownData is the storage class for all render-information
    for the addon 'Dropdown'.
    """
    @override
    def __add__(self, extraData: tuple[DropdownCO, RenderStyle]) -> 'DropdownData':
        return self

    @override
    def __mul__(self, extraData: tuple[DropdownPrefab, RenderStyle]) -> 'DropdownData':
        return self

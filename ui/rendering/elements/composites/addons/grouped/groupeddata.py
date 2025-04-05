from dataclasses import dataclass
from typing import override

from .....style      import RenderStyle
from ....atoms       import AtomCreateOption
from ..addondata     import AddonData
from .groupedcreateoption import GroupedCO
from .groupedprefab   import GroupedPrefab

@dataclass
class GroupedData(AddonData[GroupedCO, GroupedPrefab]):
    """
    GroupedData is the storage class for all render-information
    for the addon 'Grouped'.
    """

    @override
    def __add__(self, extraData: tuple[GroupedCO | AtomCreateOption, RenderStyle]) -> 'GroupedData':
        return self

    @override
    def __mul__(self, extraData: tuple[GroupedPrefab, RenderStyle]) -> 'GroupedData':
        return self

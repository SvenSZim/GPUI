from dataclasses import dataclass
from typing import override

from .....style      import RenderStyle
from ....atoms       import AtomCreateOption
from ..addondata     import AddonData
from .stackedcreateoption import StackedCO
from .stackedprefab   import StackedPrefab

@dataclass
class StackedData(AddonData[StackedCO, StackedPrefab]):
    """
    StackedData is the storage class for all render-information
    for the addon 'Stacked'.
    """

    @override
    def __add__(self, extraData: tuple[StackedCO | AtomCreateOption, RenderStyle]) -> 'StackedData':
        return self

    @override
    def __mul__(self, extraData: tuple[StackedPrefab, RenderStyle]) -> 'StackedData':
        return self

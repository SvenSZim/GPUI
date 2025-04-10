from dataclasses import dataclass
from typing import override

from .....style      import RenderStyle
from ....atoms       import AtomCreateOption
from ..addondata     import AddonData
from .stackcreateoption import StackCO
from .stackprefab   import StackPrefab

@dataclass
class StackData(AddonData[StackCO, StackPrefab]):
    """
    StackData is the storage class for all render-information
    for the addon 'Stack'.
    """

    @override
    def __add__(self, extraData: tuple[StackCO | AtomCreateOption, RenderStyle]) -> 'StackData':
        return self

    @override
    def __mul__(self, extraData: tuple[StackPrefab, RenderStyle]) -> 'StackData':
        return self

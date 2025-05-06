from dataclasses import dataclass
from typing import override

from .....style             import RenderStyle
from ....atoms              import AtomCreateOption
from ..interactabledata     import InteractableData
from .togglewrappercreateoption  import TogglewrapperCO
from .togglewrapperprefab        import TogglewrapperPrefab

@dataclass
class TogglewrapperData(InteractableData[TogglewrapperCO, TogglewrapperPrefab]):
    """
    TogglewrapperData is the storage class for all render-information
    for the interactable 'Togglewrapper'.
    """

    @override
    def __add__(self, extraData: tuple[TogglewrapperCO | AtomCreateOption, RenderStyle]) -> 'TogglewrapperData':
        return self

    @override
    def __mul__(self, extraData: tuple[TogglewrapperPrefab, RenderStyle]) -> 'TogglewrapperData':
        return self

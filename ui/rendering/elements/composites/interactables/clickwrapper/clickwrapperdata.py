from dataclasses import dataclass
from typing import override

from .....style             import RenderStyle
from ....atoms              import AtomCreateOption
from ..interactabledata     import InteractableData
from .clickwrappercreateoption  import ClickwrapperCO
from .clickwrapperprefab        import ClickwrapperPrefab

@dataclass
class ClickwrapperData(InteractableData[ClickwrapperCO, ClickwrapperPrefab]):
    """
    ClickwrapperData is the storage class for all render-information
    for the interactable 'Clickwrapper'.
    """

    @override
    def __add__(self, extraData: tuple[ClickwrapperCO | AtomCreateOption, RenderStyle]) -> 'ClickwrapperData':
        return self

    @override
    def __mul__(self, extraData: tuple[ClickwrapperPrefab, RenderStyle]) -> 'ClickwrapperData':
        return self
